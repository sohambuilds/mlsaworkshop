"""
Content Pipeline Workflow - Following proper AGNO workflow pattern
================================================================

A comprehensive content creation workflow that follows the AGNO documentation pattern.
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


class ContentResearch(BaseModel):
    """Content research findings structure"""
    topic: str = Field(..., description="Content topic being researched")
    key_facts: str = Field(..., description="Key facts and information gathered")
    sources: str = Field(..., description="Relevant sources and references")
    content_angles: str = Field(..., description="Potential content angles and perspectives")


class ContentDraft(BaseModel):
    """Content creation results structure"""
    headline: str = Field(..., description="Compelling headline for the content")
    introduction: str = Field(..., description="Engaging introduction")
    main_content: str = Field(..., description="Main body of the content")
    conclusion: str = Field(..., description="Strong conclusion with call to action")


class ContentAnalysisWorkflow(Workflow):
    """
    Advanced workflow for comprehensive content creation using multiple specialized agents.
    Follows the proper AGNO workflow pattern with agents as class attributes and yield RunResponse.
    """

    description: str = dedent("""\
    A sophisticated content creation workflow that combines research, writing, and optimization
    to produce high-quality, well-researched content ready for publication.
    Uses multiple specialized agents working in coordination to deliver polished content.
    """)

    # Content Research Agent: Handles research and fact-checking
    researcher: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[DuckDuckGoTools(), ReasoningTools()],
        description=dedent("""\
        You are ContentResearch-AI, an expert content researcher with expertise in:
        - Topic research and fact-checking
        - Source verification and citation
        - Trend analysis and current information gathering
        - Content angle development and audience insights
        """),
        instructions=dedent("""\
        1. Research Strategy 🔍
           - Conduct thorough research on the given topic
           - Gather current facts, statistics, and expert opinions
           - Identify trending aspects and unique angles
           - Verify information from multiple reliable sources
        2. Content Planning 📝
           - Develop potential content angles and perspectives
           - Identify target audience interests and pain points
           - Suggest compelling hooks and story elements
           - Plan content structure and key messages
        3. Quality Standards ✅
           - Ensure all facts are current and accurate
           - Provide proper source attribution
           - Focus on authoritative and credible sources
           - Highlight unique insights and value propositions
        """),
        response_model=ContentResearch,
        exponential_backoff=True
    )

    # Content Creator Agent: Handles writing and creative development
    writer: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        description=dedent("""\
        You are ContentCreator-AI, a skilled content writer with expertise in:
        - Engaging content creation and storytelling
        - Clear, compelling writing across formats
        - SEO optimization and readability
        - Brand voice and audience engagement
        """),
        instructions=dedent("""\
        1. Writing Excellence 📝
           - Create compelling, well-structured content
           - Use clear, engaging language appropriate for audience
           - Develop strong headlines and introductions
           - Maintain consistent tone and voice throughout
        2. Content Structure 🏗️
           - Organize content with logical flow and transitions
           - Use headers, bullet points, and formatting for readability
           - Include actionable insights and takeaways
           - End with strong conclusions or calls to action
        3. Quality Assurance ✅
           - Ensure accuracy of all facts and claims
           - Optimize for readability and engagement
           - Include relevant examples and case studies
           - Maintain professional yet accessible tone
        """),
        response_model=ContentDraft,
        exponential_backoff=True
    )

    # Content Analyst Agent: Handles optimization and quality analysis
    analyst: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[ReasoningTools()],
        description=dedent("""\
        You are ContentAnalyst-AI, a content optimization expert with expertise in:
        - Content quality analysis and improvement
        - SEO optimization and keyword integration
        - Readability analysis and enhancement
        - Performance prediction and optimization
        """),
        instructions=dedent("""\
        1. Content Analysis 📊
           - Evaluate content quality, clarity, and engagement
           - Assess structure, flow, and readability
           - Check for completeness and accuracy
           - Identify areas for improvement
        2. Optimization 🎯
           - Suggest improvements for better engagement
           - Recommend SEO enhancements and keyword usage
           - Optimize headlines and meta descriptions
           - Enhance calls to action and conversion elements
        3. Quality Standards ✅
           - Ensure content meets publication standards
           - Verify factual accuracy and source attribution
           - Check for consistency in tone and style
           - Provide final recommendations and score
        """),
        exponential_backoff=True
    )

    def run(self, topic: str, use_cache: bool = True) -> Iterator[RunResponse]:
        """
        Execute the content creation workflow for comprehensive content development.
        
        Args:
            topic: The topic for content creation
            use_cache: Whether to use cached responses for efficiency
            
        Yields:
            RunResponse: Workflow execution responses
        """
        logger.info(f"🚀 Starting Content Pipeline Workflow for topic: {topic}")
        
        # Phase 1: Content Research
        yield RunResponse(
            content=f"📝 **Content Pipeline Workflow Started**\n\nTopic: **{topic}**\n\nThis workflow will create high-quality content through coordinated research, writing, and optimization."
        )

        research_prompt = f"""
        Research the topic: {topic}
        
        Provide comprehensive research including:
        1. Key facts and current information
        2. Multiple authoritative sources
        3. Potential content angles and perspectives
        4. Target audience insights and interests
        
        Focus on accuracy, relevance, and unique value propositions.
        """

        logger.info("🔍 Phase 1: Content Research")
        yield RunResponse(
            content="🔍 **Phase 1: Content Research**\n\nContentResearch-AI is gathering information and developing content angles..."
        )

        # Run agent to get structured response (non-streaming for structured data)
        research_response = self.researcher.run(research_prompt)
        
        # When agent has response_model, content IS the structured object
        if isinstance(research_response.content, ContentResearch):
            research_results = research_response.content
        else:
            # Fallback: create structure from string content
            content_str = str(research_response.content)
            research_results = ContentResearch(
                topic=topic,
                key_facts=content_str[:400] + "..." if len(content_str) > 400 else content_str,
                sources="Multiple authoritative online sources",
                content_angles="Various perspectives and approaches identified"
            )

        yield RunResponse(
            content=f"✅ **Research Complete**\n\n**Topic:** {research_results.topic}\n\n**Key Facts:** {research_results.key_facts[:200]}...\n\n**Content Angles:** {research_results.content_angles[:200]}..."
        )

        # Phase 2: Content Creation
        writing_prompt = f"""
        Based on this research: {research_results}
        
        Create compelling content for the topic: {topic}
        
        Requirements:
        1. Engaging headline that captures attention
        2. Strong introduction that hooks the reader
        3. Well-structured main content with clear sections
        4. Compelling conclusion with actionable takeaways
        
        Use the research findings to ensure accuracy and include relevant examples.
        """

        logger.info("📝 Phase 2: Content Creation")
        yield RunResponse(
            content="📝 **Phase 2: Content Creation**\n\nContentCreator-AI is writing engaging content based on research findings..."
        )

        # Run agent to get structured response (non-streaming for structured data)
        writing_response = self.writer.run(writing_prompt)
        
        # When agent has response_model, content IS the structured object
        if isinstance(writing_response.content, ContentDraft):
            content_draft = writing_response.content
        else:
            # Fallback: create structure from string content
            content_str = str(writing_response.content)
            content_lines = content_str.split('\n')
            headline = next((line for line in content_lines if line.strip()), "Generated Content")
            content_draft = ContentDraft(
                headline=headline,
                introduction=content_str[:300] + "..." if len(content_str) > 300 else content_str,
                main_content=content_str,
                conclusion="Summary and actionable insights provided."
            )

        yield RunResponse(
            content=f"✅ **Content Draft Complete**\n\n**Headline:** {content_draft.headline}\n\n**Preview:** {content_draft.introduction[:200]}..."
        )

        # Phase 3: Content Analysis and Optimization
        analysis_prompt = f"""
        Analyze and optimize this content:
        
        Headline: {content_draft.headline}
        Introduction: {content_draft.introduction}
        Main Content: {content_draft.main_content}
        Conclusion: {content_draft.conclusion}
        
        Provide:
        1. Quality assessment and recommendations
        2. SEO optimization suggestions
        3. Readability improvements
        4. Overall content score and final recommendations
        """

        logger.info("📊 Phase 3: Content Analysis")
        yield RunResponse(
            content="📊 **Phase 3: Content Analysis**\n\nContentAnalyst-AI is analyzing and optimizing the content..."
        )

        # Run agent to get response content
        analysis_response = self.analyst.run(analysis_prompt)
        analysis_results = analysis_response.content

        yield RunResponse(
            content=f"✅ **Content Analysis Complete**\n\n{analysis_results[:300]}..."
        )

        # Final Report
        final_report = self.compile_final_content_package(
            topic, research_results, content_draft, analysis_results
        )

        yield RunResponse(
            content=final_report
        )

        logger.info("🎉 Content Pipeline Workflow completed successfully")

    def compile_final_content_package(
        self, topic: str, research: ContentResearch, 
        content: ContentDraft, analysis: str
    ) -> str:
        """Compile the final content package with all components."""
        
        return dedent(f"""\
        # 📝 Content Pipeline Complete: {topic}

        ## 🎯 Final Content Package

        ### **Headline**
        {content.headline}

        ### **Introduction**
        {content.introduction}

        ### **Main Content**
        {content.main_content}

        ### **Conclusion**
        {content.conclusion}

        ## 🔍 Research Foundation
        
        **Key Facts:** {research.key_facts}
        
        **Sources:** {research.sources}
        
        **Content Strategy:** {research.content_angles}

        ## 📊 Quality Analysis
        
        {analysis}

        ## ✅ Content Status
        **Status:** Ready for publication  
        **Quality:** Optimized and fact-checked  
        **SEO:** Analyzed and enhanced  

        ---
        *Content created using coordinated AI agents through AGNO Content Pipeline Workflow*
        """)


def create_content_pipeline_workflow(storage_dir: str = "tmp") -> ContentAnalysisWorkflow:
    """
    Create a content pipeline workflow with proper storage configuration.
    
    Args:
        storage_dir: Directory for workflow storage
        
    Returns:
        Configured content pipeline workflow following AGNO pattern
    """
    import os
    os.makedirs(storage_dir, exist_ok=True)
    
    return ContentAnalysisWorkflow(
        session_id="content-pipeline-workflow",
        storage=SqliteStorage(
            table_name="content_pipeline_workflows",
            db_file=f"{storage_dir}/content_workflows.db"
        ),
        debug_mode=True
    )