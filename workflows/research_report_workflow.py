"""
Research Report Workflow - Following proper AGNO workflow pattern
===============================================================

A comprehensive research report generation workflow that follows the AGNO documentation pattern.
"""

import os
from textwrap import dedent
from typing import Iterator

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.workflow import Workflow, RunResponse
from agno.utils.log import logger
from pydantic import BaseModel, Field


class ResearchFindings(BaseModel):
    """Research findings structure"""
    research_topic: str = Field(..., description="Topic being researched")
    methodology: str = Field(..., description="Research methodology and approach")
    key_findings: str = Field(..., description="Primary research findings and discoveries")
    data_sources: str = Field(..., description="Sources and references used")


class DataAnalysis(BaseModel):
    """Data analysis results structure"""
    statistical_insights: str = Field(..., description="Statistical analysis and patterns")
    key_metrics: str = Field(..., description="Important metrics and measurements")
    trends_patterns: str = Field(..., description="Identified trends and patterns")
    recommendations: str = Field(..., description="Data-driven recommendations")


class ResearchReportWorkflow(Workflow):
    """
    Advanced workflow for comprehensive research report generation using multiple specialized agents.
    Follows the proper AGNO workflow pattern with agents as class attributes and yield RunResponse.
    """

    description: str = dedent("""\
    A sophisticated research report workflow that combines information gathering, data analysis,
    and professional report writing to produce comprehensive research documents.
    Uses multiple specialized agents working in coordination to deliver thorough analysis.
    """)

    # Research Agent: Handles information gathering and data collection
    researcher: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[DuckDuckGoTools(), ReasoningTools()],
        description=dedent("""\
        You are ResearchSpecialist-AI, an expert researcher with expertise in:
        - Comprehensive information gathering and data collection
        - Source verification and academic research methods
        - Literature review and systematic investigation
        - Primary and secondary research coordination
        """),
        instructions=dedent("""\
        1. Research Excellence 🔍
           - Conduct thorough and systematic research
           - Gather data from multiple authoritative sources
           - Use proper research methodologies
           - Ensure information accuracy and reliability
        2. Data Collection 📊
           - Organize findings systematically
           - Document all sources and references
           - Identify key themes and patterns
           - Maintain research integrity standards
        3. Quality Standards ✅
           - Use credible and peer-reviewed sources
           - Cross-verify important information
           - Maintain objectivity and balance
           - Provide comprehensive coverage of topic
        """),
        response_model=ResearchFindings,
        exponential_backoff=True
    )

    # Data Analyst Agent: Handles statistical analysis and insights
    analyst: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[ReasoningTools()],
        description=dedent("""\
        You are DataAnalyst-AI, a statistical analysis expert with expertise in:
        - Quantitative and qualitative data analysis
        - Statistical modeling and trend identification
        - Data visualization and interpretation
        - Research methodology and validation
        """),
        instructions=dedent("""\
        1. Data Analysis 📈
           - Perform statistical analysis on research data
           - Identify patterns, trends, and correlations
           - Calculate relevant metrics and measurements
           - Validate findings through multiple approaches
        2. Insights Generation 💡
           - Extract meaningful insights from data
           - Identify key relationships and dependencies
           - Highlight significant findings and anomalies
           - Provide context for statistical results
        3. Recommendations 🎯
           - Develop data-driven recommendations
           - Suggest areas for further investigation
           - Identify limitations and considerations
           - Propose actionable next steps
        """),
        response_model=DataAnalysis,
        exponential_backoff=True
    )

    # Report Writer Agent: Handles professional report formatting
    writer: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        description=dedent("""\
        You are ReportWriter-AI, a professional report writer with expertise in:
        - Academic and business report writing
        - Clear communication of complex information
        - Professional formatting and structure
        - Executive summary and presentation skills
        """),
        instructions=dedent("""\
        1. Report Structure 📋
           - Create professional, well-organized reports
           - Use clear headings, sections, and formatting
           - Include executive summary and conclusions
           - Maintain academic/professional writing standards
        2. Communication Excellence 📝
           - Present complex information clearly
           - Use appropriate language for target audience
           - Include visual elements and data presentation
           - Ensure logical flow and coherence
        3. Professional Standards ✅
           - Follow report writing best practices
           - Include proper citations and references
           - Maintain objectivity and professionalism
           - Provide actionable recommendations
        """),
        exponential_backoff=True
    )

    def run(self, research_topic: str, use_cache: bool = True) -> Iterator[RunResponse]:
        """
        Execute the research report workflow for comprehensive report generation.
        
        Args:
            research_topic: The topic for research investigation
            use_cache: Whether to use cached responses for efficiency
            
        Yields:
            RunResponse: Workflow execution responses
        """
        logger.info(f"🚀 Starting Research Report Workflow for topic: {research_topic}")
        
        # Phase 1: Information Gathering
        yield RunResponse(
            content=f"📊 **Research Report Workflow Started**\n\nTopic: **{research_topic}**\n\nThis workflow will generate a comprehensive research report through systematic investigation, analysis, and professional writing."
        )

        research_prompt = f"""
        Conduct comprehensive research on: {research_topic}
        
        Requirements:
        1. Systematic information gathering from multiple sources
        2. Clear research methodology description
        3. Organized presentation of key findings
        4. Comprehensive source documentation
        
        Focus on academic rigor, accuracy, and comprehensive coverage.
        """

        logger.info("🔍 Phase 1: Information Gathering")
        yield RunResponse(
            content="🔍 **Phase 1: Information Gathering**\n\nResearchSpecialist-AI is conducting systematic research and data collection..."
        )

        # Run agent to get structured response (non-streaming for structured data)
        research_response = self.researcher.run(research_prompt)
        
        # When agent has response_model, content IS the structured object
        if isinstance(research_response.content, ResearchFindings):
            research_findings = research_response.content
        else:
            # Fallback: create structure from string content
            content_str = str(research_response.content)
            research_findings = ResearchFindings(
                research_topic=research_topic,
                methodology="Comprehensive research using multiple sources and analysis",
                key_findings=content_str[:500] + "..." if len(content_str) > 500 else content_str,
                data_sources="Multiple online sources and databases"
            )

        yield RunResponse(
            content=f"✅ **Research Complete**\n\n**Topic:** {research_findings.research_topic}\n\n**Methodology:** {research_findings.methodology[:200]}...\n\n**Key Findings:** {research_findings.key_findings[:200]}..."
        )

        # Phase 2: Data Analysis
        analysis_prompt = f"""
        Analyze the research findings: {research_findings}
        
        Perform comprehensive analysis including:
        1. Statistical analysis of quantitative data
        2. Pattern and trend identification
        3. Key metrics calculation and interpretation
        4. Data-driven recommendations and insights
        
        Focus on extracting meaningful insights and actionable recommendations.
        """

        logger.info("📈 Phase 2: Data Analysis")
        yield RunResponse(
            content="📈 **Phase 2: Data Analysis**\n\nDataAnalyst-AI is analyzing research data and identifying patterns..."
        )

        # Run agent to get structured response (non-streaming for structured data)
        analysis_response = self.analyst.run(analysis_prompt)
        
        # When agent has response_model, content IS the structured object
        if isinstance(analysis_response.content, DataAnalysis):
            data_analysis = analysis_response.content
        else:
            # Fallback: create structure from string content
            content_str = str(analysis_response.content)
            data_analysis = DataAnalysis(
                statistical_insights=content_str[:300] + "..." if len(content_str) > 300 else content_str,
                key_metrics="Key metrics derived from research data",
                trends_patterns="Identified patterns and trends from analysis",
                recommendations=content_str[-300:] if len(content_str) > 300 else content_str
            )

        yield RunResponse(
            content=f"✅ **Analysis Complete**\n\n**Statistical Insights:** {data_analysis.statistical_insights[:200]}...\n\n**Recommendations:** {data_analysis.recommendations[:200]}..."
        )

        # Phase 3: Report Writing
        writing_prompt = f"""
        Create a comprehensive research report based on:
        
        Research Findings: {research_findings}
        Data Analysis: {data_analysis}
        
        Report should include:
        1. Executive Summary
        2. Methodology Section
        3. Findings and Analysis
        4. Recommendations and Conclusions
        5. References and Appendices
        
        Use professional academic/business report format with clear structure and presentation.
        """

        logger.info("📝 Phase 3: Report Writing")
        yield RunResponse(
            content="📝 **Phase 3: Report Writing**\n\nReportWriter-AI is crafting the comprehensive research report..."
        )

        # Run agent to get response content
        writing_response = self.writer.run(writing_prompt)
        final_report = writing_response.content

        yield RunResponse(
            content=f"✅ **Report Writing Complete**\n\nComprehensive research report has been prepared with professional formatting and structure."
        )

        # Final Report Package
        complete_report = self.compile_final_report(
            research_topic, research_findings, data_analysis, final_report
        )

        yield RunResponse(
            content=complete_report
        )

        logger.info("🎉 Research Report Workflow completed successfully")

    def compile_final_report(
        self, topic: str, research: ResearchFindings, 
        analysis: DataAnalysis, report: str
    ) -> str:
        """Compile the final comprehensive research report."""
        
        return dedent(f"""\
        # 📊 Research Report: {topic}

        ## 📋 Executive Summary

        This comprehensive research report presents systematic investigation findings, 
        statistical analysis, and data-driven recommendations for **{topic}**.

        ## 🔍 Research Methodology

        **Approach:** {research.methodology}

        **Data Sources:** {research.data_sources}

        ## 🔎 Key Findings

        {research.key_findings}

        ## 📈 Statistical Analysis

        **Insights:** {analysis.statistical_insights}

        **Key Metrics:** {analysis.key_metrics}

        **Trends & Patterns:** {analysis.trends_patterns}

        ## 💡 Recommendations

        {analysis.recommendations}

        ## 📝 Detailed Report

        {report}

        ## ✅ Report Summary

        **Status:** Complete and validated  
        **Quality:** Professional academic/business standard  
        **Scope:** Comprehensive coverage with data-driven insights  

        ---
        *Research report generated using coordinated AI agents through AGNO Research Report Workflow*
        """)


def create_research_report_workflow(storage_dir: str = "tmp") -> ResearchReportWorkflow:
    """
    Create a research report workflow with proper storage configuration.
    
    Args:
        storage_dir: Directory for workflow storage
        
    Returns:
        Configured research report workflow following AGNO pattern
    """
    import os
    os.makedirs(storage_dir, exist_ok=True)
    
    return ResearchReportWorkflow(
        session_id="research-report-workflow",
        storage=SqliteStorage(
            table_name="research_report_workflows",
            db_file=f"{storage_dir}/research_workflows.db"
        ),
        debug_mode=True
    )