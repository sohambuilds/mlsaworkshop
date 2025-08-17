import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.sqlite import SqliteStorage
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.arxiv import ArxivTools
from pathlib import Path




def create_research_agent(storage_dir: str = "tmp") -> Agent:


    Path(storage_dir).mkdir(exist_ok=True)
   
    return Agent(
        name="Research Specialist",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[GoogleSearchTools(
            # stop_after_tool_call_tools=["google_search"],
            # show_result_tools=["google_search"],
        ),ArxivTools()],
        instructions=[
            "You are a research specialist with web search capabilities",
            "Always Search the web using google search tools to find what you need"
            "Always cite your sources with URLs when possible",
            "Provide comprehensive and up-to-date information",
            "Fact-check claims using multiple sources",
            "Present information in a clear, organized manner",
            "Include relevant context and background information"
        ],
        storage=SqliteStorage(
            table_name="research_agent",
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











