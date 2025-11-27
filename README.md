# SkillMatch AI: Optimized Job Search, Scoring & CV Tailoring 🌟

## Project Overview
SkillMatch AI is a robust, multi-agent system designed to streamline the job application process. 
Built using the Google Agent Development Kit (ADK), this project demonstrates:

- Advanced agent orchestration using SequentialAgent
- Dual Model Context Protocol (MCP) integration
- Sophisticated memory management
- Automatic generation of ATS-optimized CVs and application packages

------------------------------------------------------------

## 🔧 Key Functionality

1. Job Search  
   Autonomous discovery of job listings via an external MCP service.

2. Scoring  
   Match scoring (0–100%) between the user's CV and job requirements.

3. Tailoring  
   Generation of an ATS-friendly CV + application package using a second MCP server.

------------------------------------------------------------

## ⚙️ Architecture Pipeline (SequentialAgent)

1. JobSearchAgent — Finds job listings  
   Output: job_search_results

2. ResumeParsingAgent — Parses the user's CV  
   Output: parsed_resume_json

3. JobScoringAgent — Computes match scores and selects Top 3  
   Output: most_relevant_jobs

4. TailoredATSCvCreatorAgent — Produces the final tailored CV  
   Output: PDF and application package

------------------------------------------------------------

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Google ADK +Google GenAI(pip install google-adk google-genai)
- Node.js + npm
- Gemini API Key

------------------------------------------------------------

## Step 1: Clone the Repository

git clone https://github.com/Oumarkei/capstone_project_google_x_kaggle.git
cd CapstoneProject

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

------------------------------------------------------------

## Step 2: Configure Environment Variables

Create a .env file at inside job_search_agents:

# Your Gemini API Key
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

# Path to the resume file used by ResumeParsingAgent
# Example: job_search_agents/CV_Oumar_KEITA_Junior_DS.pdf
RESUME_PATH=""

------------------------------------------------------------

## Step 3: Set Up the CV Forge MCP Server (Crucial)
Inside the root folder :
git clone https://github.com/thechandanbhagat/cv-forge.git
cd cv-forge

npm install
npm run build

# Return to main project
cd ..

⚠️ Important:
Ensure the path inside all_tools_mcp_sv.py matches the actual location of the cv-forge folder.
Update the cwd variable if necessary.

------------------------------------------------------------

## Step 4: Run the Full Pipeline

python job_search_agents/final_agents.py

------------------------------------------------------------

## Step 5: Run the Development UI (MVP Agent)

adk web --port 8000

Then open:
http://127.0.0.1:8000

------------------------------------------------------------

## 👤 Created By
Oumar KEITA, Data Scientist - Industrial Management Engineer 
Built for the Google x Kaggle 5-Day AI Agents Intensive Capstone Project.
