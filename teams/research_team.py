import os
from agno.team import Team
from agno.models.google import Gemini
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent
from agents.content_agent import create_content_agent




def create_research_team(storage_dir: str = "tmp") -> Team:


   
    # Create team members
    researcher = create_research_agent(storage_dir)
    analyst = create_analysis_agent(storage_dir)
    writer = create_content_agent(storage_dir)
   
    # Create coordinated team with rate limiting
    team = Team(
        name="Research Investigation Team",
        description="A team of specialists for comprehensive research and analysis projects",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        members=[researcher, analyst, writer],
        instructions=[
            "You are a research team that works together to investigate topics thoroughly",
            "The Research Specialist gathers information from web sources",
            "The Data Analyst processes numerical data and performs calculations",
            "The Content Creator organizes findings into clear, well-structured reports",
            "Coordinate your efforts to provide comprehensive, accurate analysis",
            "Always cite sources and show your work",
            "Present findings in a clear, professional format",
            "Work patiently - allow time between responses to respect API limits"
        ],
        # Coordination mode - agents work together towards a common goal
        show_tool_calls=True,
        # Note: Rate limiting is handled by individual agents, not teams
    )
   
    return team

