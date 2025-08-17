"""
Market Analysis Workflow - Following proper AGNO workflow pattern
================================================================

A comprehensive market analysis workflow that follows the AGNO documentation pattern.
"""

import os
import json
from textwrap import dedent
from typing import Iterator, Optional

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools
from agno.workflow import Workflow, RunResponse
from agno.utils.log import logger
from pydantic import BaseModel, Field


class MarketResearch(BaseModel):
    """Market research findings structure"""
    company: str = Field(..., description="Company being analyzed")
    industry_analysis: str = Field(..., description="Industry trends and competitive landscape")
    market_position: str = Field(..., description="Company's market position and competitive advantages")
    growth_prospects: str = Field(..., description="Growth opportunities and market trends")


class FinancialMetrics(BaseModel):
    """Financial analysis results structure"""
    stock_performance: str = Field(..., description="Recent stock performance and trends")
    key_ratios: str = Field(..., description="Important financial ratios and metrics")
    valuation: str = Field(..., description="Valuation analysis and fair value assessment")
    financial_health: str = Field(..., description="Overall financial strength assessment")


class MarketAnalysisWorkflow(Workflow):
    """
    Advanced workflow for comprehensive market analysis using multiple specialized agents.
    Follows the proper AGNO workflow pattern with agents as class attributes and yield RunResponse.
    """

    description: str = dedent("""\
    A sophisticated market analysis workflow that combines market research,
    financial analysis, and risk assessment to provide comprehensive investment insights.
    Uses multiple specialized agents working in coordination to deliver thorough analysis.
    """)

    # Market Research Agent: Handles web search and competitive analysis
    researcher: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[DuckDuckGoTools(), ReasoningTools()],
        description=dedent("""\
        You are MarketResearch-AI, an elite market research specialist with expertise in:
        - Industry analysis and competitive intelligence
        - Market positioning and trend identification
        - Business model evaluation and strategic assessment
        - Comprehensive company and sector research
        """),
        instructions=dedent("""\
        1. Research Strategy 🔍
           - Conduct thorough company and industry research
           - Analyze competitive landscape and market positioning
           - Identify growth drivers and market opportunities
           - Gather recent news and developments
        2. Analysis Focus 📊
           - Business model and revenue streams
           - Competitive advantages and market share
           - Industry trends and growth prospects
           - Key strategic initiatives and partnerships
        3. Output Quality ✅
           - Provide structured, actionable insights
           - Include specific data points and examples
           - Highlight key strategic considerations
           - Cite relevant sources and timeframes
        """),
        response_model=MarketResearch,
        exponential_backoff=True,
        delay_between_retries=2
    )

    # Financial Analysis Agent: Handles quantitative financial data
    finance_analyst: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[YFinanceTools(), ReasoningTools()],
        description=dedent("""\
        You are FinanceAnalyst-AI, a financial analysis expert specializing in:
        - Quantitative financial analysis and metrics evaluation
        - Stock performance and valuation assessment
        - Financial health and profitability analysis
        - Investment recommendation and risk evaluation
        """),
        instructions=dedent("""\
        1. Financial Analysis 💰
           - Analyze recent stock performance and price trends
           - Calculate and interpret key financial ratios
           - Assess valuation using multiple methodologies
           - Evaluate financial strength and liquidity
        2. Data Integration 📈
           - Use real-time market data and financial information
           - Compare performance with industry benchmarks
           - Identify financial strengths and potential risks
           - Analyze revenue trends and profitability metrics
        3. Investment Perspective 🎯
           - Provide clear valuation assessment
           - Highlight key financial performance drivers
           - Identify potential red flags or concerns
           - Suggest monitoring metrics and thresholds
        """),
        response_model=FinancialMetrics,
        exponential_backoff=True,
        delay_between_retries=2
    )

    # Risk Assessment Agent: Synthesizes analysis into actionable insights
    risk_analyst: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[ReasoningTools()],
        description=dedent("""\
        You are RiskAnalyst-AI, a senior investment analyst specializing in:
        - Comprehensive risk assessment and scenario analysis
        - Investment recommendation synthesis
        - Risk-adjusted return evaluation
        - Strategic investment guidance
        """),
        instructions=dedent("""\
        1. Risk Analysis ⚠️
           - Evaluate market, financial, and operational risks
           - Assess competitive threats and industry disruption
           - Analyze regulatory and macroeconomic factors
           - Quantify risk-return trade-offs
        2. Synthesis & Recommendations 💡
           - Integrate market research and financial analysis
           - Provide clear investment thesis and rationale
           - Suggest appropriate position sizing and timing
           - Identify key catalysts and risk factors
        3. Action-Oriented Output 🎯
           - Clear buy/hold/sell recommendation with reasoning
           - Specific price targets and risk levels
           - Key monitoring metrics and trigger points
           - Portfolio allocation suggestions
        """),
        markdown=True,
        exponential_backoff=True,
        delay_between_retries=2
    )

    def run(
        self,
        company: str,
        use_search_cache: bool = True,
        use_financial_cache: bool = True,
        use_cached_report: bool = True,
    ) -> Iterator[RunResponse]:
        """
        Execute comprehensive market analysis workflow for the specified company.
        
        Args:
            company: Company symbol or name to analyze
            use_search_cache: Whether to use cached market research
            use_financial_cache: Whether to use cached financial analysis
            use_cached_report: Whether to use cached complete report
        """
        logger.info(f"Starting market analysis for: {company}")

        # Check for cached complete analysis
        if use_cached_report:
            cached_analysis = self.get_cached_analysis(company)
            if cached_analysis:
                yield RunResponse(content=cached_analysis)
                return

        # Step 1: Market Research Phase
        yield RunResponse(content=f"🔍 **Starting Market Analysis for {company}**")
        yield RunResponse(content="## 📊 Phase 1: Market Research & Competitive Analysis")
        
        market_research = self.get_market_research(company, use_search_cache)
        if not market_research:
            yield RunResponse(content=f"❌ Could not complete market research for {company}. Analysis terminated.")
            return

        yield RunResponse(content=f"""
### ✅ Market Research Complete
- **Company**: {market_research.company}
- **Industry Analysis**: {market_research.industry_analysis[:150]}...
- **Market Position**: {market_research.market_position[:150]}...
- **Growth Prospects**: {market_research.growth_prospects[:150]}...
""")

        # Step 2: Financial Analysis Phase
        yield RunResponse(content="## 💰 Phase 2: Financial Analysis & Valuation")
        
        financial_metrics = self.get_financial_analysis(company, use_financial_cache)
        if not financial_metrics:
            yield RunResponse(content="⚠️ Limited financial data available. Proceeding with qualitative analysis.")
            financial_metrics = FinancialMetrics(
                stock_performance="Limited data available - requires manual analysis",
                key_ratios="Unable to retrieve comprehensive metrics",
                valuation="Qualitative assessment needed",
                financial_health="Assessment incomplete - manual review required"
            )

        yield RunResponse(content=f"""
### ✅ Financial Analysis Complete
- **Stock Performance**: {financial_metrics.stock_performance[:150]}...
- **Key Ratios**: {financial_metrics.key_ratios[:150]}...
- **Valuation**: {financial_metrics.valuation[:150]}...
- **Financial Health**: {financial_metrics.financial_health[:150]}...
""")

        # Step 3: Risk Assessment & Final Recommendations
        yield RunResponse(content="## ⚖️ Phase 3: Risk Assessment & Investment Recommendations")
        
        # Prepare comprehensive input for risk analyst
        analysis_input = {
            "company": company,
            "market_research": market_research.model_dump(),
            "financial_metrics": financial_metrics.model_dump()
        }

        risk_prompt = f"""
        Based on the comprehensive research below, provide a detailed investment analysis and recommendations for {company}:

        **Market Research:**
        {json.dumps(market_research.model_dump(), indent=2)}

        **Financial Analysis:**
        {json.dumps(financial_metrics.model_dump(), indent=2)}

        **Required Analysis:**
        1. **Risk Assessment**: Identify and quantify key risks (market, financial, operational)
        2. **Investment Thesis**: Clear bull/bear case with supporting evidence
        3. **Recommendation**: Specific buy/hold/sell with price targets and rationale
        4. **Portfolio Considerations**: Position sizing and timing recommendations
        5. **Monitoring Plan**: Key metrics and catalysts to watch

        Provide actionable investment guidance with clear reasoning.
        """

        # Run risk analysis and yield streaming response
        yield from self.risk_analyst.run(risk_prompt, stream=True)

        # Compile and cache final report
        final_report = self.compile_final_report(
            company, market_research, financial_metrics, self.risk_analyst.run_response.content
        )
        
        self.cache_analysis(company, final_report)

        yield RunResponse(
            content="## 📋 Analysis Complete - Full Report Generated"
        )

    def get_cached_analysis(self, company: str) -> Optional[str]:
        """Retrieve cached complete analysis if available."""
        return self.session_state.get("complete_analyses", {}).get(company)

    def cache_analysis(self, company: str, analysis: str):
        """Cache the complete analysis results."""
        self.session_state.setdefault("complete_analyses", {})
        self.session_state["complete_analyses"][company] = analysis

    def get_market_research(self, company: str, use_cache: bool) -> Optional[MarketResearch]:
        """Get market research data with caching."""
        # Check cache first
        if use_cache:
            cached = self.session_state.get("market_research", {}).get(company)
            if cached:
                try:
                    return MarketResearch.model_validate(cached)
                except Exception as e:
                    logger.warning(f"Could not validate cached market research: {e}")

        # Conduct new research
        try:
            research_prompt = f"""
            Conduct comprehensive market research for {company}:
            
            1. **Company Analysis**: Business model, core operations, revenue streams
            2. **Industry Analysis**: Trends, growth drivers, competitive dynamics
            3. **Market Position**: Competitive advantages, market share, differentiation
            4. **Growth Prospects**: Opportunities, expansion plans, market trends
            
            Provide structured analysis with specific insights and data.
            """
            
            response = self.researcher.run(research_prompt)
            if response and response.content and isinstance(response.content, MarketResearch):
                # Cache the research
                self.session_state.setdefault("market_research", {})
                self.session_state["market_research"][company] = response.content.model_dump()
                return response.content
        except Exception as e:
            logger.error(f"Market research failed: {e}")
        
        return None

    def get_financial_analysis(self, company: str, use_cache: bool) -> Optional[FinancialMetrics]:
        """Get financial analysis data with caching."""
        # Check cache first
        if use_cache:
            cached = self.session_state.get("financial_analysis", {}).get(company)
            if cached:
                try:
                    return FinancialMetrics.model_validate(cached)
                except Exception as e:
                    logger.warning(f"Could not validate cached financial analysis: {e}")

        # Conduct new analysis
        try:
            financial_prompt = f"""
            Perform comprehensive financial analysis for {company}:
            
            1. **Stock Performance**: Recent price trends, volatility, trading patterns
            2. **Key Ratios**: P/E, P/S, ROE, debt ratios, profitability metrics
            3. **Valuation**: Fair value estimate, comparison to peers, valuation methods
            4. **Financial Health**: Balance sheet strength, cash flow, liquidity analysis
            
            Use real-time financial data and provide quantitative insights.
            """
            
            response = self.finance_analyst.run(financial_prompt)
            if response and response.content and isinstance(response.content, FinancialMetrics):
                # Cache the analysis
                self.session_state.setdefault("financial_analysis", {})
                self.session_state["financial_analysis"][company] = response.content.model_dump()
                return response.content
        except Exception as e:
            logger.error(f"Financial analysis failed: {e}")
        
        return None

    def compile_final_report(
        self, company: str, market_research: MarketResearch, 
        financial_metrics: FinancialMetrics, risk_assessment: str
    ) -> str:
        """Compile comprehensive investment analysis report."""
        return f"""
# 📈 Comprehensive Investment Analysis: {company}

## 🎯 Executive Summary
Multi-agent analysis completed using specialized AGNO workflow combining market research, financial analysis, and risk assessment.

---

## 🔍 Market Research & Intelligence
**Company**: {market_research.company}

**Industry Analysis**:
{market_research.industry_analysis}

**Market Position**:
{market_research.market_position}

**Growth Prospects**:
{market_research.growth_prospects}

---

## 💰 Financial Analysis & Valuation
**Stock Performance**:
{financial_metrics.stock_performance}

**Key Financial Ratios**:
{financial_metrics.key_ratios}

**Valuation Assessment**:
{financial_metrics.valuation}

**Financial Health**:
{financial_metrics.financial_health}

---

## ⚖️ Risk Assessment & Investment Recommendations
{risk_assessment}

---

## 🤖 Analysis Methodology
**Workflow**: AGNO Multi-Agent Investment Analysis
**Agents Used**: 
- MarketResearch-AI: Web search + competitive intelligence
- FinanceAnalyst-AI: YFinance data + quantitative analysis  
- RiskAnalyst-AI: Synthesis + investment recommendations

**Models**: Gemini 1.5 Flash with exponential backoff
**Tools**: DuckDuckGo Search, YFinance, Reasoning Tools

*Analysis completed for {company} using coordinated AI agents*
        """


def create_market_analysis_workflow(storage_dir: str = "tmp") -> MarketAnalysisWorkflow:
    """
    Create a market analysis workflow with proper storage configuration.
    
    Args:
        storage_dir: Directory for workflow storage
        
    Returns:
        Configured market analysis workflow following AGNO pattern
    """
    import os
    os.makedirs(storage_dir, exist_ok=True)
    
    return MarketAnalysisWorkflow(
        session_id="market-analysis-workflow",
        storage=SqliteStorage(
            table_name="market_analysis_workflows",
            db_file=f"{storage_dir}/market_workflows.db"
        ),
        debug_mode=True
    )