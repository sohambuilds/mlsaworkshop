#!/usr/bin/env python3
"""
AGNO Workshop Playground - Agents, Teams & Workflows
====================================================

Comprehensive playground showcasing individual agents, coordinated teams,
and complex workflows using the AGNO framework.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

try:
    from agno.playground import Playground
    
    # Import our structured components
    from agents import (
        create_research_agent,
        create_finance_agent,
        create_content_agent,
        create_analysis_agent
    )
    from teams import (
        create_research_team,
        create_business_team,
        create_creative_team
    )
    from workflows import (
        create_market_analysis_workflow,
        create_content_pipeline_workflow,
        create_research_report_workflow,
        create_academic_research_workflow
    )
    
    print("✅ AGNO Workshop components imported successfully")
    
    # Import rate limiting configuration
    from rate_limit_config import print_rate_limit_info
    print_rate_limit_info()
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Please set your GEMINI_API_KEY in .env file")
        print("Get your key from: https://aistudio.google.com/")
        exit(1)
    
    # Setup storage directory
    storage_dir = "tmp"
    Path(storage_dir).mkdir(exist_ok=True)
    
    print("🤖 Creating individual agents...")
    # Create individual specialist agents
    research_agent = create_research_agent(storage_dir)
    finance_agent = create_finance_agent(storage_dir) 
    content_agent = create_content_agent(storage_dir)
    analysis_agent = create_analysis_agent(storage_dir)
    
    individual_agents = [research_agent, finance_agent, content_agent, analysis_agent]
    print(f"✅ Created {len(individual_agents)} individual agents")
    
    print("👥 Creating coordinated teams...")
    # Create coordinated teams
    research_team = create_research_team(storage_dir)
    business_team = create_business_team(storage_dir)
    creative_team = create_creative_team(storage_dir)
    
    teams = [research_team, business_team, creative_team]
    print(f"✅ Created {len(teams)} specialized teams")
    
    print("🔄 Creating AGNO workflows...")
    # Create proper AGNO workflows
    market_workflow = create_market_analysis_workflow(storage_dir)
    content_workflow = create_content_pipeline_workflow(storage_dir) 
    research_workflow = create_research_report_workflow(storage_dir)
    academic_workflow = create_academic_research_workflow(storage_dir)
    
    workflows = [market_workflow, content_workflow, research_workflow, academic_workflow]
    print(f"✅ Created {len(workflows)} AGNO workflows")
    
    # Create playground with agents, teams, AND workflows
    print(f"🎮 Creating playground with:")
    print(f"   - {len(individual_agents)} individual agents")
    print(f"   - {len(teams)} coordinated teams")
    print(f"   - {len(workflows)} AGNO workflows")
    
    # Create comprehensive playground with all components
    playground_app = Playground(
        agents=individual_agents,
        teams=teams,
        workflows=workflows
    )
    app = playground_app.get_app()
    
    print("✅ Playground created successfully")
    
    if __name__ == "__main__":
        print("\n🌟 Starting AGNO Workshop Playground...")
        print("📱 Look for the live AGNO playground link below!")
        print("\n🎯 Available in the playground:")
        print("   🤖 Individual Agents:")
        print("      - Research Specialist (web search)")
        print("      - Finance Expert (market data)")
        print("      - Content Creator (writing)")
        print("      - Data Analyst (calculations)")
        print("\n   👥 Coordinated Teams:")
        print("      - Research Investigation Team")
        print("      - Business Intelligence Team")
        print("      - Creative Content Team")
        print("\n   🔄 AGNO Workflows (integrated):")
        print("      - Market Analysis Workflow: Comprehensive investment analysis")
        print("      - Content Pipeline Workflow: Research to publication pipeline")
        print("      - Research Report Workflow: Academic/business report generation")
        print("      - Academic Research Workflow: Literature validation (Workflows v2)")
        print("\n⚠️  Press Ctrl+C to stop the playground")
        
        # Use exact method from documentation to get live link
        playground_app.serve("playground:app", reload=False)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Install dependencies:")
    print("uv add agno google-generativeai duckduckgo-search yfinance sqlalchemy 'fastapi[standard]'")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Troubleshooting:")
    print("1. Ensure all dependencies are installed: uv sync")
    print("2. Check your GEMINI_API_KEY in .env file")
    print("3. Verify AGNO version: pip show agno")
    print("4. Try running individual agent files first")
