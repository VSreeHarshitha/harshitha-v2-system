import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool

# Internal imports from your project structure
from app.schemas.portfolio_models import PortfolioUpdate
from app.services.n8n_service import trigger_n8n_workflow

# 1. Setup the LLM (Gemini 1.5 Flash for speed and tool-calling accuracy)
# Ensure GOOGLE_API_KEY is set in your backend/.env file
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    streaming=True, 
    temperature=0.7
)

# 2. Define the "Update" Tool
@tool
def update_portfolio_tool(update_data: dict):
    """
    Use this tool to update Sree Harshitha's portfolio information.
    The update_data should be a dictionary matching the PortfolioUpdate schema.
    """
    try:
        # Validate data using your Pydantic model
        validated_data = PortfolioUpdate(**update_data)

        # Trigger n8n workflow (running the async service in a sync wrapper)
        result = asyncio.run(trigger_n8n_workflow(
            validated_data, 
            admin_id="Sree_Harshitha_Admin"
        ))
        return result
    except Exception as e:
        return f"Validation Error: {str(e)}. Please ask the user for correct data (e.g., CGPA must be 0-10)."

# 3. Create the Agent Prompt
# This system prompt defines the "personality" of your portfolio brain
system_prompt = (
    "You are Sree Harshitha's Portfolio Manager. You are professional, tech-savvy, and witty. "
    "Sree is a 3rd-year AIML student at Malla Reddy University, a member of the 'Dakshin Loka' band, "
    "and a Microsoft Learn Student Ambassador. "
    "You can update her portfolio using the update_portfolio_tool. "
    "If a user wants to change her CGPA, projects, or skills, you MUST use the tool. "
    "If they provide invalid data, gently guide them to the correct format."
)

# 4. Construct the Agent (The Correct 2026 Pattern)
tools = [update_portfolio_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Replaces the undefined 'create_agent'
agent = create_tool_calling_agent(llm, tools, prompt)

# The agent_executor is what your FastAPI main.py will actually call
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)