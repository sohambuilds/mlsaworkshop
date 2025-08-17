"""
Finance Agent - Market Analysis and Financial Data
==================================================

Specialized agent for financial analysis, stock market data, and investment insights.
"""

import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.storage.sqlite import SqliteStorage
from pathlib import Path


def create_calculator_agent(storage_dir: str = "tmp") -> Agent:

    Path(storage_dir).mkdir(exist_ok=True)
    
    return Agent(
        name="Finance Expert",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True, 
            company_info=True,
            company_news=True,
            historical_prices=True
        )],
        instructions=[
            "You are a financial analyst with access to real-time market data",
            "Always use tables to display financial data clearly",
            "Provide context and analysis with your data",
            "Explain financial metrics in accessible terms",
            "Include risk considerations in your analysis",
            "Cite data sources and timestamps",
            "Highlight key trends and patterns in the data"
        ],
        storage=SqliteStorage(
            table_name="finance_agent",
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
