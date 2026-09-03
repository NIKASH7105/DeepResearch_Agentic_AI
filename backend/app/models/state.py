"""
Agent state model for LangGraph
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ToolCall(BaseModel):
    """Record of a tool invocation"""
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    success: bool = True
    error_message: Optional[str] = None


class ResearchState(BaseModel):
    """
    State maintained throughout the research process
    This is the core state object passed through LangGraph nodes
    """
    # Session Information
    session_id: str
    user_query: str
    research_goal: Optional[str] = None
    research_depth: str = "standard"
    
    # Planning
    research_plan: List[str] = Field(default_factory=list)
    current_task: Optional[str] = None
    completed_tasks: List[str] = Field(default_factory=list)
    
    # Tool Usage
    tool_history: List[ToolCall] = Field(default_factory=list)
    available_tools: List[str] = Field(default_factory=list)
    
    # Research Data
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    claims: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Analysis
    conflicts: List[Dict[str, Any]] = Field(default_factory=list)
    research_gaps: List[str] = Field(default_factory=list)
    verification_results: Dict[str, Any] = Field(default_factory=dict)
    
    # Synthesis
    key_findings: List[str] = Field(default_factory=list)
    synthesis: Optional[str] = None
    
    # Report
    final_report: Optional[str] = None
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Control Flow
    iteration_count: int = 0
    max_iterations: int = 10
    needs_more_research: bool = True
    is_complete: bool = False
    
    # Metadata
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
