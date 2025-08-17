"""


A team focused on creative projects, content strategy, and storytelling.
"""

import os
from agno.team import Team
from agno.models.google import Gemini
from agents.content_agent import create_content_agent
from agents.research_agent import create_research_agent
from agents.analysis_agent import create_analysis_agent


def create_creative_team(storage_dir: str = "tmp") -> Team:

    
    # Create team members
    content_creator = create_content_agent(storage_dir)
    researcher = create_research_agent(storage_dir)
    analyst = create_analysis_agent(storage_dir)
    
 
    team = Team(
        name="Creative Content Team", 
        description="A team of creatives for content strategy and storytelling projects",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        members=[content_creator, researcher, analyst],
        instructions=[
            "You are a creative team focused on content strategy and storytelling",
            "The Content Creator leads creative writing, storytelling, and content development",
            "The Research Specialist provides background research, fact-checking, and context",
            "The Data Analyst helps with content optimization, audience analysis, and performance metrics",
            "Collaborate to create engaging, well-researched, and effective content",
            "Balance creativity with accuracy and audience needs",
            "Provide multiple creative options and iterations",
            "Focus on storytelling that resonates with the intended audience",
            "Take your time - allow space between responses to respect API limits"
        ],
        show_tool_calls=True,
       
    )
    
    return team
