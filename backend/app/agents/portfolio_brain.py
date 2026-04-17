import os
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, RunContext
from app.services.n8n_service import trigger_n8n_workflow


# 1. Define the Structured Schema (The "Rules")
class PortfolioUpdate(BaseModel):
    field: str = Field(
        description="The part of the site to update (e.g., 'cgpa', 'bio', 'projects')"
    )
    new_value: str = Field(
        description="The new content to display"
    )
    reasoning: str = Field(
        description="Why the AI is suggesting this change"
    )

    @field_validator('new_value')
    @classmethod
    def validate_cgpa(cls, v: str, info) -> str:
        # If updating CGPA, ensure it's valid (0–10)
        if info.data.get('field') == 'cgpa':
            try:
                score = float(v)
                if not (0 <= score <= 10):
                    raise ValueError("CGPA must be between 0 and 10")
            except ValueError:
                raise ValueError("Invalid CGPA format. Please provide a number.")
        return v


# 2. Initialize the Pydantic AI Agent (FIXED VERSION)
portfolio_agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt=(
        "You are Sree Harshitha's Portfolio Manager, an AI built for 'Project P'. "
        "Harshitha is a 3rd-year AIML student at Malla Reddy University and lead vocalist for 'Dakshin Loka'. "
        "You help manage her portfolio updates intelligently. "
        "If a user asks to change CGPA, projects, or bio, use the 'update_portfolio' tool. "
        "Always be professional, slightly witty, and highly technical."
    ),
)


# 3. Define the Tool (The "Action")
@portfolio_agent.tool
async def update_portfolio(ctx: RunContext[None], update_data: PortfolioUpdate) -> str:
    """
    Triggers a portfolio update request.
    Sends notification via n8n workflow (e.g., WhatsApp approval).
    """
    try:
        result = await trigger_n8n_workflow(
            update_data,
            admin_id="Sree_Harshitha_Admin"
        )
        return f"✅ Update request sent for '{update_data.field}'. Status: {result}"
    except Exception as e:
        return f"❌ Error triggering update: {str(e)}"


@portfolio_agent.tool
async def get_current_stats(ctx: RunContext[None]) -> str:
    """
    Returns the current live status of the portfolio.
    """
    return "📊 Current CGPA: 9.5 | 🎤 Band: Dakshin Loka | 🚀 Milestone: MLSA Alpha"