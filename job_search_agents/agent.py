# Let's import necessary modules from google ADK
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.genai import types
from google.adk.models.google_llm import Gemini


# Let's import our predefined tools, MCP servers
from job_search_agents.all_tools_mcp_sv import resume_parser, mcp_jobsearch_server, mcp_tailoredcv_server

# Let's load environment variables (specifically the resume path)
import os
from dotenv import load_dotenv
load_dotenv()

resume_path = os.getenv("RESUME_PATH", "/Users/mac/Documents/CapstoneProject/job_search_agents/CV_Oumar_KEITA_Junior_DS.pdf")

# Let's define retry configurations
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# Job Search Agent
job_search_agent = Agent(
    model=Gemini(model = 'gemini-2.5-flash-lite',retry_options= retry_config),
    name='JobSearchAgent',
    description='A Job Search Agent that can find relevant job based on user queries.',
    instruction=""" You are **JobSearchAgent**, an AI Job Search Specialist.
            Your mission is to find the most relevant, high-quality and up-to-date opportunities that match the user’s criteria (skills, experience, etc...).
            Use the MCP Job Search Server to search for jobs based on user preferences.

            Your output should be in human readable format and include the following information for each job found in these orders:
            - Company Name
            - Job Title
            - Requirements (e.g., the experience required, familiarity with specific tools or technologies, etc...)
            - Education Level
            - Key Skills
            - Link to apply for the job
            
            You must follow these guidelines: 
            1. Adapt to the user's language (English or French).
            2. Provide results only when the user has given clear job preferences (you can help them formulate theiir query if necessary).
            3. If the user’s request is vague or incomplete, ask for clarification first (help them if possible).
            4. Only return information that is returned by the Job Search MCP Server.
            5. Do not fabricate any information.
            6. If the tool returns no results, politely inform the user and suggest how to refine the query.
            7. Return all the jobs found in a JSON array format.
            8. Never include commentary outside the final response.
            9. Don't use complex technical jargon; keep it simple and clear.
            10. Be polite, concise, and professional in your responses.

                    """,
    tools= [mcp_jobsearch_server],
    output_key= "job_search_results",
)
# Resume Parsing Agent
resume_parsing_agent = Agent(
    name = "ResumeParsingAgent",
    model = Gemini(model = 'gemini-2.5-flash-lite',retry_options= retry_config),
    description = "An agent that extracts structured information from the user's resume.",
    instruction = f"""Your sole task is to use the 'resume_parser' tool on the resume located at {resume_path} and return the entire resume information.
                    Do not add any commentary, only return the output from the tool and display it.""",
    tools = [resume_parser],
    output_key= "parsed_resume_json", # Clé pour transférer l'information
)

# Job Scoring Agent - Rendre l'instruction plus abstraite
job_scoring_agent = Agent(
    name = "JobScoringAgent",
    model = Gemini(model = 'gemini-2.5-flash',retry_options= retry_config),
    description = "An agent that computes a match score between a user's resume and a job description.",
    instruction =""" You are **JobScoringAgent**, an AI specialist in job macthing score computation.
                Your task is to compute a match score (0-100%) between the user's resume and each job description.

                **Use the JSON data provided in the variable 'parsed_resume_json' as the user's qualifications.**
                **Use the JSON array provided in the variable 'job_search_results' as the list of jobs to be scored.**

                You must give a match score by yourself based on the job requirements and the detailed resume information. Focus on understanding job context and user's qualifications.

                The output must be a JSON array containing the top 3 jobs with the highest match scores. Each job object in the array must include all original job details PLUS a 'match_score' key.
                """,
    
    output_key= "most_relevant_jobs",
)
tailored_cv_creator_agent = Agent(
    name = "TailoredATSCvCreatorAgent",
    model = Gemini(model = 'gemini-2.5-flash',retry_options= retry_config),
    description = "An agent that creates a tailored ATS-friendly CV for a specific job description.",
    instruction=""" You are **TailoredATSCvCreatorAgent**, an AI specialist in creating tailored ATS-friendly CVs.
                Your task is to create a tailored ATS-friendly CV based on the user's resume and a specific job description.

                **Use the only the JSON data provided in the variable 'parsed_resume_json' as the user's qualifications.**
                **Use only the most relevant job (the job with the highest match score) description in the variable 'most_relevant_jobs' as the target job for CV creation.**

                You must focus on aligning the user's qualifications with the job requirements to enhance ATS compatibility.

                The output must be a well-structured ATS-friendly CV in PDF that highlights relevant skills, experiences, and keywords from the job description.
                
                For this task, use the MCP Tailored CV Server tool to generate the CV in PDF format. Make sure the server receives all necessary information to create an effective CV.
                
                You must return and save the generated CV to the indicated path (Mandatory!) and a message indicating the successful creation of the tailored CV.
                If you cannot create the CV or the server doesn't return anything, mention it.
    """,
    tools= [mcp_tailoredcv_server],
    output_key= "tailored_ats_cv_pdf",
)
# Sequential Job Search Agent
root_agent = SequentialAgent(
    name = "JobSearchAndScoringAgentPipeline",
    description = "A sequential agent that orchestrates job search, resume parsing, job scoring, and tailored CV creatior agents.",
    sub_agents= [
        job_search_agent, # 1. Cherche les jobs (produit {{job_search_results}})
        resume_parsing_agent, # 2. Parse le CV (produit {{parsed_resume_json}})
        job_scoring_agent, # 3. Score les jobs en utilisant les deux clés précédentes,
        tailored_cv_creator_agent, # 4. Crée un CV adapté au job le plus pertinent
    ],
)