"""
AGNO Workshop Workflows
======================

This module contains proper AGNO Workflow classes that follow the framework pattern.
These workflows inherit from the Workflow class and yield RunResponse objects.
"""

from .market_analysis_workflow import create_market_analysis_workflow, MarketAnalysisWorkflow
from .content_pipeline_workflow import create_content_pipeline_workflow, ContentAnalysisWorkflow 
from .research_report_workflow import create_research_report_workflow, ResearchReportWorkflow
from .academic_research_workflow import create_academic_research_workflow

__all__ = [
    'create_market_analysis_workflow',
    'create_content_pipeline_workflow', 
    'create_research_report_workflow',
    'create_academic_research_workflow',
    'MarketAnalysisWorkflow',
    'ContentAnalysisWorkflow',
    'ResearchReportWorkflow'
]
