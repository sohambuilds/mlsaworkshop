# MLSA KIIT: Captcha the Imposter Workshop

A comprehensive hands-on workshop demonstrating AI agent orchestration using the **AGNO** framework. This workshop covers individual agents, coordinated teams, and complex workflows for real-world AI applications.

## 🎯 Workshop Overview

This workshop introduces participants to building sophisticated AI systems using:
- **Individual Agents**: Specialized AI agents for specific tasks
- **Coordinated Teams**: Multiple agents working together
- **AGNO Workflows**: Complex multi-step AI processes
- **Real-world Integration**: Web search, financial data, content creation

## 🏗️ Project Structure

```
📁 NGMI25/Workshop/
├── 🎮 playground.py              # Main application entry point
├── 📋 pyproject.toml             # Project dependencies and configuration
├── 🔒 uv.lock                    # Dependency lock file
├── 📁 agents/                    # Individual AI agents
│   ├── 🤖 analysis_agent.py     # Data analysis and calculations
│   ├── 🤖 content_agent.py      # Creative writing and content creation  
│   ├── 🤖 finance_agent.py      # Financial data and market analysis
│   ├── 🤖 research_agent.py     # 🚧 Workshop exercise (empty)
│   └── 📄 __init__.py
├── 📁 teams/                     # Coordinated agent teams
│   ├── 👥 business_team.py      # Business intelligence team
│   ├── 👥 creative_team.py      # Creative content team
│   ├── 👥 research_team.py      # 🚧 Workshop exercise (empty)
│   └── 📄 __init__.py
├── 📁 workflows/                 # AGNO workflow orchestrations
│   ├── 🔄 academic_research_workflow.py    # Academic research pipeline
│   ├── 🔄 content_pipeline_workflow.py    # Content creation workflow
│   ├── 🔄 market_analysis_workflow.py     # Market analysis workflow
│   ├── 🔄 research_report_workflow.py     # Research report generation
│   └── 📄 __init__.py
└── 📁 tmp/                       # SQLite databases and temporary files
    ├── 💾 agents.db              # Agent conversation history
    ├── 💾 market_workflows.db    # Market workflow data
    ├── 💾 content_workflows.db   # Content workflow data
    └── 💾 research_workflows.db  # Research workflow data
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+** installed
2. **uv package manager** 
3. **Gemini API key** from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/sohambuilds/mlsaworkshop.git
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   ```

3. **Set up your API key:**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```

4. **Run the playground:**
   ```bash
   # Using uv
   uv run playground.py
   
   ```

5. **Access the web interface:**
   - Open your browser to the provided playground URL
   - Interact with agents, teams, and workflows through the web UI

## 🤖 Available Components

### Individual Agents

| Agent | Purpose | Tools & Capabilities |
|-------|---------|---------------------|
| **Research Specialist** | 🚧 *Workshop Exercise* | Web search, data gathering |
| **Finance Expert** | Market analysis & financial data | YFinance API, stock data, financial metrics |
| **Content Creator** | Creative writing & content | Storytelling, copywriting, content strategy |
| **Data Analyst** | Calculations & analysis | Mathematical computations, data processing |

### Coordinated Teams

| Team | Members | Use Cases |
|------|---------|-----------|
| **Research Investigation Team** | 🚧 *Workshop Exercise* | Academic research, fact-checking |
| **Business Intelligence Team** | Research + Finance + Analysis | Market research, investment analysis |
| **Creative Content Team** | Content + Research + Analysis | Content marketing, storytelling |

### AGNO Workflows

| Workflow | Purpose | Complexity |
|----------|---------|------------|
| **Market Analysis** | Investment research & analysis | Advanced |
| **Content Pipeline** | Research → Writing → Publishing | Intermediate |
| **Research Report** | Academic/business report generation | Advanced |
| **Academic Research** | Literature review & validation | Expert |

## 🛠️ Technology Stack

### Core Framework
- **[AGNO](https://docs.agno.ai/)**: AI Agent Network Orchestration framework
- **[Google Gemini 2.0](https://ai.google.dev/)**: Advanced language model
- **[FastAPI](https://fastapi.tiangolo.com/)**: Web framework for playground UI

### Agent Tools & Integrations
- **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)**: Web search capabilities
- **[YFinance](https://pypi.org/project/yfinance/)**: Financial data and stock market API
- **[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)**: Web scraping and parsing
- **[arXiv](https://pypi.org/project/arxiv/)**: Academic paper research
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: Database ORM for conversation persistence

### Development & Deployment
- **[UV](https://docs.astral.sh/uv/)**: Fast Python package manager
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)**: Environment variable management
- **[SQLite](https://www.sqlite.org/)**: Local database for agent memory

## 🎓 Workshop Exercises

### Exercise 1: Build Research Agent
**File:** `agents/research_agent.py`

**Objective:** Create a research agent with web search capabilities

**Requirements:**
- Use DuckDuckGo search tools
- Implement proper error handling
- Add conversation memory with SQLite storage
- Configure rate limiting for API calls


### Exercise 2: Build Research Team
**File:** `teams/research_team.py`

**Objective:** Create a coordinated team for research tasks

**Requirements:**
- Combine research agent with other specialists
- Define clear team roles and coordination
- Implement team-level instructions
- Handle multi-agent conversations


## 🔧 Configuration & Customization

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

```

### Rate Limiting
The project includes built-in rate limiting to prevent API quota issues:
- **Exponential backoff**: Automatically retries with increasing delays
- **Delay between retries**: 2-second minimum delay
- **Request throttling**: Manages concurrent API calls

### Storage & Memory
- **SQLite databases**: Store conversation history and agent memory
- **Separate tables**: Each agent/team/workflow has isolated storage
- **Persistent sessions**: Conversations survive application restarts

## 🌟 Key Features Demonstrated

### 1. Agent Specialization
- **Domain expertise**: Each agent specializes in specific tasks
- **Tool integration**: Agents use appropriate external APIs and services
- **Memory persistence**: Agents remember conversation context

### 2. Team Coordination
- **Role definition**: Clear responsibilities for each team member
- **Communication protocols**: Structured interaction patterns
- **Collective intelligence**: Teams produce better results than individual agents

### 3. Workflow Orchestration
- **Multi-step processes**: Complex tasks broken into manageable steps
- **Data flow**: Structured information passing between workflow stages
- **Error handling**: Robust handling of failures and edge cases

### 4. Real-world Integration
- **Live data sources**: Real-time web search and financial data
- **API management**: Proper handling of external service limitations
- **Scalable architecture**: Designed for production-level usage



## 🐛 Troubleshooting

### Common Issues

**1. API Key Issues**
```bash
❌ Please set your GEMINI_API_KEY in .env file
```
**Solution:** Create `.env` file with valid Gemini API key

**2. Import Errors**
```bash
❌ Import error: No module named 'agno'
```
**Solution:** Install dependencies: `uv sync` or `pip install -r requirements.txt`

**3. Rate Limit Errors**
```bash
❌ API rate limit exceeded
```
**Solution:** Built-in rate limiting should handle this automatically

**4. Database Lock Errors**
```bash
❌ Database is locked
```
**Solution:** Close other instances of the application

### Debug Mode
Enable detailed logging:
```bash
export AGNO_LOG_LEVEL=DEBUG
uv run playground.py
```

## 📚 Learning Resources

### AGNO Framework Documentation
- **[Official AGNO Docs](https://docs.agno.ai/)**: Complete framework documentation
- **[Agent Development](https://docs.agno.ai/agents/)**: Building individual agents  
- **[Team Coordination](https://docs.agno.ai/teams/)**: Multi-agent collaboration
- **[Workflow Orchestration](https://docs.agno.ai/workflows/)**: Complex process automation

### AI & LLM Resources
- **[Google Gemini API](https://ai.google.dev/)**: Language model capabilities
- **[Prompt Engineering](https://developers.google.com/machine-learning/resources/prompt-eng)**: Writing effective prompts
- **[AI Agent Patterns](https://www.deeplearning.ai/)**: Agent architecture patterns

## 🤝 Contributing

This workshop codebase is designed for learning and experimentation:

1. **Fork the repository** for your own experiments
2. **Complete the workshop exercises** in the designated files
3. **Extend the examples** with your own agents and workflows
4. **Share your creations** with the workshop community

## 📝 License

This workshop material is provided for educational purposes. Please respect the terms of service for all integrated APIs and services:

- **Google Gemini API**: [Terms of Service](https://ai.google.dev/terms)
- **DuckDuckGo**: [Privacy Policy](https://duckduckgo.com/privacy)
- **Yahoo Finance**: [Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html)

## 🔗 Workshop Resources

- **Organizer**: MLSA KIIT
- **Framework**: [AGNO Documentation](https://docs.agno.ai/)
- **API Keys**: [Google AI Studio](https://aistudio.google.com/)
- **Support**: Your nearest FAQ Team member!

---

**Happy Agent Building!** 🤖✨

*Built with ❤️ for the MLSA KIIT Captcha the Imposter Agentic AI Workshop*