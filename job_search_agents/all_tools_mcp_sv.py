from resumeparser_pro import ResumeParserPro
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Let's define the job search MCP Server
mcp_jobsearch_server = McpToolset(
    connection_params= StdioConnectionParams(
        server_params= StdioServerParameters(
            command = "npx",
            args  = [
                "-y",
                "mcp-remote@latest",
                "https://jobswithgpt.com/mcp"
            ]
        ),
        timeout= 300,
    )
)

# Let's define the Tailored CV MCP Server
mcp_tailoredcv_server = McpToolset(
    connection_params= StdioConnectionParams(
        server_params= StdioServerParameters(
            command = "node",
            args  = [
                "build/index.js"
            ],
            cwd= "/Users/mac/Documents/CapstoneProject/cv-forge",
            env = {
                "DEFAULT_OUTPUT_PATH": "/Users/mac/Documents/CapstoneProject/",
                "PDF_BASE_FONT_SIZE": "12px",
                "PDF_LINE_HEIGHT": "1.4",
            },
            #tool_filter= ["generate_and_save_cv_pdf","generate_cv_pdf"]
        ),
        timeout= 300,
    )
)

# Let's define the Resume Parser tool
def resume_parser(resume_path : "str") -> dict:
    """
    Parse resumes in various formats such as PDF, DOCX, and TXT to extract its information.
    Args:
        resume_path (str): the path to the resume file to be parsed.

    Returns:
        A Dictionary containing the extracted information from the resume.
    """
    # Initialize the parser with your chosen AI provider and API key
    parser = ResumeParserPro(
        provider="google_genai",
        model_name="gemini-2.5-flash-lite", 
        api_key=GOOGLE_API_KEY
    )
    
    # Parse the resume
    
    try :
        result = parser.parse_resume(resume_path)
        return result.model_dump()
    except Exception as e:
        return {"error": str(e)}
        
