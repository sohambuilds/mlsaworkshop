
import os
from agno.team import Team
from agno.models.google import Gemini
from agents.research_agent import create_research_agent
from agents.finance_agent import create_finance_agent
from agents.analysis_agent import create_analysis_agent


def create_business_team(storage_dir: str = "tmp") -> Team:

    # Create team members
    researcher = create_research_agent(storage_dir)
    finance_expert = create_finance_agent(storage_dir)
    analyst = create_analysis_agent(storage_dir)
    
    # Create business intelligence team with rate limiting
    team = Team(
        name="Business Intelligence Team",
        description="A team of business experts for market research and financial analysis",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        members=[researcher, finance_expert, analyst],
        instructions=[
            "You are a business intelligence team focused on market research and financial analysis",
            "The Research Specialist handles market research, competitor analysis, and industry trends",
            "The Finance Expert analyzes financial data, stock performance, and investment metrics",
            "The Data Analyst processes business metrics, performs calculations, and identifies patterns",
            "Work together to provide comprehensive business insights",
            "Focus on actionable recommendations and data-driven insights",
            "Present analysis in business-friendly formats with clear conclusions",
            "Coordinate efficiently - allow time between responses to respect API limits"
        ],
        show_tool_calls=True,
        # Note: Rate limiting is handled by individual agents, not teams
    )
    
    return team
