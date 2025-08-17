"""
Content Agent - Creative Writing and Content Creation
=====================================================

Specialized agent for creative writing, content creation, and storytelling.
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from pathlib import Path


def create_content_agent(storage_dir: str = "tmp") -> Agent:

    Path(storage_dir).mkdir(exist_ok=True)
    
    return Agent(
        name="Content Creator",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        instructions=[
            "You are a creative writing and content creation specialist",
            "Help with storytelling, copywriting, and creative projects",
            "Provide engaging, well-structured content",
            "Adapt your writing style to the audience and purpose",
            "Offer multiple creative options and variations",
            "Include practical tips for content improvement",
            "Be imaginative while maintaining clarity and purpose"
        ],
        storage=SqliteStorage(
            table_name="content_agent",
            db_file=f"{storage_dir}/agents.db"
        ),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
        show_tool_calls=True,
        # Rate limiting configuration
        exponential_backoff=True,
        delay_between_retries=2, 
    )
