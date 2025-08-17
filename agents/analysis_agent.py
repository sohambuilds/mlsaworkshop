

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.storage.sqlite import SqliteStorage
from pathlib import Path


def create_analysis_agent(storage_dir: str = "tmp") -> Agent:

    Path(storage_dir).mkdir(exist_ok=True)
    
    return Agent(
        name="Data Analyst",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[ReasoningTools()],
        instructions=[
            "You are a data analyst and mathematical reasoning specialist",
            "Solve complex mathematical problems step by step",
            "Use reasoning tools for accurate calculations",
            "Present analysis in clear, logical formats",
            "Explain your reasoning process thoroughly", 
            "Identify patterns and trends in data",
            "Provide statistical insights and interpretations",
            "Use tables and charts to visualize results when helpful"
        ],
        storage=SqliteStorage(
            table_name="analysis_agent",
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
