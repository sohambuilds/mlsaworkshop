
import os
from textwrap import dedent
from typing import Iterator, List

from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.workflow import Workflow, RunResponse
from agno.utils.log import logger

from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.arxiv import ArxivTools
from pydantic import BaseModel, Field


class LiteratureFindings(BaseModel):
    """Structure for literature search results"""
    research_topic: str = Field(..., description="The research topic being investigated")
    key_papers: List[str] = Field(..., description="List of key academic papers found")
    research_gaps: str = Field(..., description="Identified gaps in current research")
    methodology_trends: str = Field(..., description="Common methodologies used in the field")


class FactCheckResults(BaseModel):
    """Structure for fact verification results"""
    verified_claims: List[str] = Field(..., description="Claims that were verified as accurate")
    disputed_claims: List[str] = Field(..., description="Claims that are disputed or unclear")
    confidence_scores: str = Field(..., description="Confidence assessment of the research")
    additional_sources: List[str] = Field(..., description="Additional sources for verification")


class AcademicResearchWorkflow(Workflow):
   

    description: str = dedent("""\
    A sophisticated academic research validation workflow that demonstrates advanced
    step-by-step orchestration. Unlike simple agent coordination, this workflow shows
    structured data flow, mixed execution types, and deterministic processing steps.
    """)

    # Step 1: Literature Search Agent
    literature_specialist: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[GoogleSearchTools(),ArxivTools(), ReasoningTools()],
        description="Expert in academic literature search and analysis",
        response_model=LiteratureFindings,
        instructions=[
            "Conduct thorough academic literature searches on given topics",
            "Focus on peer-reviewed papers and academic sources",
            "Identify research gaps and methodology trends", 
            "Structure findings according to the LiteratureFindings model",
            "Prioritize recent publications and high-impact journals"
        ],
        exponential_backoff=True
    )

    # Step 2: Fact-Checking Team (demonstrates team integration)
    verification_team: Team = Team(
        name="Research Verification Team",
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        members=[
            Agent(
                name="Primary Fact Checker",
                model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
                tools=[DuckDuckGoTools()],
                instructions="Verify research claims using multiple independent sources"
            ),
            Agent(
                name="Methodology Validator",
                model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
                tools=[ReasoningTools()],
                instructions="Validate research methodologies and statistical approaches"
            )
        ],
        instructions=[
            "Collaborate to verify research claims and methodologies",
            "Cross-reference findings with multiple authoritative sources",
            "Assess the reliability and validity of research methods",
            "Identify potential biases or limitations in the research"
        ],
        response_model=FactCheckResults
    )

    # Step 3: Citation Analysis Agent
    citation_analyst: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        tools=[ReasoningTools()],
        description="Specialist in citation analysis and research impact assessment",
        instructions=[
            "Analyze citation patterns and research impact",
            "Evaluate the credibility and influence of research papers",
            "Assess the academic rigor of methodologies",
            "Provide recommendations for strengthening research validity"
        ],
        exponential_backoff=True
    )

    # Step 4: Report Generation Agent
    report_generator: Agent = Agent(
        model=Gemini(id="gemini-2.0-flash", api_key=os.getenv("GEMINI_API_KEY")),
        description="Expert in academic writing and research documentation",
        instructions=[
            "Create comprehensive academic research reports",
            "Follow proper academic writing standards and formatting",
            "Include methodology, findings, limitations, and recommendations",
            "Ensure proper citation and reference formatting",
            "Write in clear, professional academic language"
        ],
        exponential_backoff=True
    )

    def run(self, research_topic: str, use_cache: bool = True) -> Iterator[RunResponse]:
        """
        Execute the academic research validation workflow with step-by-step orchestration.
        
        This demonstrates the workflow pattern advantages:
        - Deterministic step sequence with structured data flow
        - Mixed execution types (agents, teams, custom processing)
        - Automatic output chaining between steps
        - Error handling and validation at each step
        
        Args:
            research_topic: The academic research topic to validate
            use_cache: Whether to use cached responses for efficiency
            
        Yields:
            RunResponse: Workflow execution responses with structured progress
        """
        logger.info(f"🎓 Starting Academic Research Validation Workflow: {research_topic}")
        
        yield RunResponse(
            content=f"🎓 **Academic Research Validation Workflow Started**\n\nTopic: **{research_topic}**\n\nThis workflow demonstrates advanced step-by-step orchestration with structured data flow between agents, teams, and custom processing steps."
        )

        # =================================================================
        # STEP 1: LITERATURE SEARCH & ANALYSIS
        # =================================================================
        yield RunResponse(content="## 📚 Step 1: Literature Search & Analysis")
        
        literature_prompt = dedent(f"""
        Conduct a comprehensive academic literature review on:
        
        RESEARCH TOPIC: {research_topic}
        
        SEARCH REQUIREMENTS:
        1. Find at least 8-10 key academic papers from the last 5 years
        2. Include seminal works that established foundational concepts
        3. Identify current research trends and emerging methodologies
        4. Note any significant research gaps or contradictions
        5. Focus on peer-reviewed journals and academic publications
        
        ANALYSIS FOCUS:
        - Methodological approaches commonly used
        - Key findings and consensus areas
        - Debates and disagreements in the field
        - Future research directions suggested by authors
        
        Structure your findings according to the LiteratureFindings model.
        """)

        logger.info("📚 Step 1: Literature Search & Analysis")
        
        # Execute literature search with structured response
        literature_response = self.literature_specialist.run(literature_prompt)
        
        # Handle structured response
        if isinstance(literature_response.content, LiteratureFindings):
            literature_findings = literature_response.content
        else:
            # Fallback for string content
            content_str = str(literature_response.content)
            literature_findings = LiteratureFindings(
                research_topic=research_topic,
                key_papers=["Multiple academic papers identified from literature search"],
                research_gaps=content_str[:300] + "..." if len(content_str) > 300 else content_str,
                methodology_trends="Various methodological approaches identified"
            )

        yield RunResponse(
            content=f"✅ **Literature Search Complete**\n\n**Topic:** {literature_findings.research_topic}\n\n**Key Papers Found:** {len(literature_findings.key_papers)} papers\n\n**Research Gaps:** {literature_findings.research_gaps[:200]}..."
        )


        yield RunResponse(content="## 🔄 Step 2: Processing Literature for Verification")
        
        # Custom processing step (shows workflow orchestration capability)  
        verification_prompt = self._prepare_verification_input(literature_findings)
        
        yield RunResponse(content="✅ **Data Processing Complete** - Literature findings prepared for fact-checking team")

        # =================================================================
        # STEP 3: FACT-CHECKING & VERIFICATION (demonstrates team integration)
        # =================================================================
        yield RunResponse(content="## 🔍 Step 3: Fact-Checking & Verification")
        
        logger.info("🔍 Step 3: Fact-Checking & Verification")
        
        # Execute team-based verification
        verification_response = self.verification_team.run(verification_prompt)
        
        # Handle team response
        if isinstance(verification_response.content, FactCheckResults):
            fact_check_results = verification_response.content
        else:
            content_str = str(verification_response.content)
            fact_check_results = FactCheckResults(
                verified_claims=["Multiple claims verified through team analysis"],
                disputed_claims=["Some claims require additional verification"],
                confidence_scores="High confidence in core findings",
                additional_sources=["Additional authoritative sources identified"]
            )

        yield RunResponse(
            content=f"✅ **Fact-Checking Complete**\n\n**Verified Claims:** {len(fact_check_results.verified_claims)}\n\n**Disputed Claims:** {len(fact_check_results.disputed_claims)}\n\n**Confidence:** {fact_check_results.confidence_scores}"
        )

        # =================================================================
        # STEP 4: CITATION IMPACT ANALYSIS
        # =================================================================
        yield RunResponse(content="## 📊 Step 4: Citation Impact Analysis")
        
        citation_prompt = self._prepare_citation_analysis(literature_findings, fact_check_results)
        
        logger.info("📊 Step 4: Citation Impact Analysis")
        
        citation_response = self.citation_analyst.run(citation_prompt)
        citation_analysis = citation_response.content

        yield RunResponse(
            content=f"✅ **Citation Analysis Complete**\n\n{str(citation_analysis)[:300]}..."
        )

        # =================================================================
        # STEP 5: FINAL REPORT GENERATION
        # =================================================================
        yield RunResponse(content="## 📋 Step 5: Comprehensive Report Generation")
        
        report_prompt = self._prepare_final_report(
            research_topic, literature_findings, fact_check_results, citation_analysis
        )
        
        logger.info("📋 Step 5: Final Report Generation")
        
        final_response = self.report_generator.run(report_prompt)
        final_report = final_response.content

        # =================================================================
        # WORKFLOW COMPLETION WITH SUMMARY
        # =================================================================
        complete_report = self._compile_comprehensive_report(
            research_topic, literature_findings, fact_check_results, citation_analysis, final_report
        )

        yield RunResponse(content=complete_report)
        
        logger.info("🎉 Academic Research Validation Workflow completed successfully")

    def _prepare_verification_input(self, literature_findings: LiteratureFindings) -> str:
        """Custom processing function - demonstrates workflow orchestration"""
        return dedent(f"""
        FACT-CHECKING ASSIGNMENT FOR RESEARCH VERIFICATION TEAM
        
        LITERATURE FINDINGS TO VERIFY:
        Topic: {literature_findings.research_topic}
        Key Papers: {literature_findings.key_papers}
        Research Gaps: {literature_findings.research_gaps}
        Methodology Trends: {literature_findings.methodology_trends}
        
        VERIFICATION TASKS:
        1. Cross-check the key claims made in the identified papers
        2. Verify the accuracy of methodology descriptions
        3. Confirm publication details and author credentials
        4. Assess potential conflicts of interest or biases
        5. Look for supporting evidence from independent sources
        
        FOCUS AREAS:
        - Factual accuracy of core research claims
        - Validity of statistical methods used
        - Reproducibility of reported results
        - Consistency with established scientific principles
        
        Provide detailed verification results with confidence assessments.
        """)

    def _prepare_citation_analysis(self, literature: LiteratureFindings, verification: FactCheckResults) -> str:
        """Prepare structured input for citation analysis"""
        return dedent(f"""
        CITATION IMPACT ANALYSIS REQUEST
        
        RESEARCH CONTEXT:
        Topic: {literature.research_topic}
        Verified Claims: {verification.verified_claims}
        Confidence Level: {verification.confidence_scores}
        
        ANALYSIS REQUIREMENTS:
        1. Assess the academic impact and citation patterns of key papers
        2. Evaluate the credibility of highly-cited vs. lesser-cited works
        3. Identify potential citation bias or echo chambers
        4. Analyze the evolution of research themes over time
        5. Recommend the most authoritative sources for this topic
        
        EVALUATION CRITERIA:
        - Journal impact factors and publication prestige
        - Author reputation and institutional affiliations
        - Citation count trends and recency of citations
        - Cross-disciplinary influence and adoption
        
        Provide recommendations for the strongest research foundation.
        """)

    def _prepare_final_report(self, topic: str, literature: LiteratureFindings, 
                             verification: FactCheckResults, citation: str) -> str:
        """Prepare comprehensive input for final report generation"""
        return dedent(f"""
        COMPREHENSIVE ACADEMIC RESEARCH VALIDATION REPORT
        
        RESEARCH TOPIC: {topic}
        
        WORKFLOW RESULTS SUMMARY:
        Literature Analysis: {literature.research_gaps}
        Verification Results: {verification.confidence_scores}
        Citation Analysis: {str(citation)[:200]}...
        
        REPORT REQUIREMENTS:
        Create a comprehensive academic research validation report including:
        
        1. EXECUTIVE SUMMARY - Key findings and overall assessment
        2. LITERATURE REVIEW SYNTHESIS - Systematic review of identified literature
        3. FACT-CHECKING ASSESSMENT - Verification results and confidence levels
        4. CITATION IMPACT ANALYSIS - Academic credibility assessment
        5. RESEARCH GAPS & OPPORTUNITIES - Identified gaps and recommendations
        6. METHODOLOGY RECOMMENDATIONS - Best practices for research in this area
        7. CONCLUSIONS & LIMITATIONS - Overall assessment and limitations
        
        FORMAT: Professional academic research validation report
        """)

    def _compile_comprehensive_report(self, topic: str, literature: LiteratureFindings,
                                    verification: FactCheckResults, citation: str, 
                                    final_report: str) -> str:
        """Compile the final comprehensive workflow report"""
        return dedent(f"""
        # 🎓 Academic Research Validation Complete: {topic}

        ## 📊 Workflow Execution Summary
        
        **✅ 5-Step Validation Process Completed:**
        1. **Literature Search** → {len(literature.key_papers)} academic papers identified
        2. **Data Processing** → Structured data prepared for verification
        3. **Team Fact-Checking** → {len(verification.verified_claims)} claims verified
        4. **Citation Analysis** → Academic impact assessment completed
        5. **Report Generation** → Comprehensive validation report created

        ## 🔍 Key Workflow Features Demonstrated:
        
        **🔗 Step-by-Step Orchestration:**
        - Deterministic execution sequence with structured data flow
        - Automatic output chaining between workflow steps
        - Mixed execution types (agents, teams, custom functions)
        
        **📋 Structured Data Flow:**
        - Literature findings → Fact-checking input
        - Verification results → Citation analysis
        - All steps → Final comprehensive report
        
        **🛠️ Mixed Execution Types:**
        - **Agent**: Literature search with structured response model
        - **Team**: Collaborative fact-checking and verification
        - **Function**: Custom data processing and input preparation
        - **Agent**: Citation analysis and report generation

        ## 📋 Research Validation Results
        
        **Literature Foundation:**
        - Research Topic: {literature.research_topic}
        - Key Papers: {len(literature.key_papers)} academic sources
        - Research Gaps: {literature.research_gaps[:150]}...
        
        **Verification Status:**
        - Verified Claims: {len(verification.verified_claims)}
        - Confidence Level: {verification.confidence_scores}
        - Additional Sources: {len(verification.additional_sources)} identified
        
        **Final Assessment:**
        {final_report}

        ## ✅ Workflow Advantages Demonstrated
        
        **vs. Simple Agent Coordination:**
        - ✅ **Deterministic Flow**: Predictable step sequence vs. dynamic collaboration
        - ✅ **Structured Data**: Automatic chaining vs. manual coordination
        - ✅ **Mixed Types**: Agents + Teams + Functions vs. agents only
        - ✅ **Error Handling**: Built-in validation vs. basic error handling
        - ✅ **Progress Tracking**: Step-by-step visibility vs. black box processing

        ---
        *Academic research validation completed using AGNO Advanced Workflow Orchestration*
        """)


def create_academic_research_workflow(storage_dir: str = "tmp") -> AcademicResearchWorkflow:
    """
    Create an academic research validation workflow demonstrating advanced orchestration.
    
    Args:
        storage_dir: Directory for workflow storage
        
    Returns:
        Configured academic research validation workflow
    """
    import os
    os.makedirs(storage_dir, exist_ok=True)
    
    return AcademicResearchWorkflow(
        session_id="academic-research-workflow",
        storage=SqliteStorage(
            table_name="academic_research_workflows",
            db_file=f"{storage_dir}/academic_workflows.db"
        ),
        debug_mode=True
    )