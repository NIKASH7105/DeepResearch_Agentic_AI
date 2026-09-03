"""
Research endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid
import os

from app.models.research import ResearchSession, ResearchDepth, ResearchStatus

router = APIRouter()

# In-memory storage for MVP (will be replaced with database)
research_sessions: dict = {}


class ResearchRequest(BaseModel):
    """Request model for starting research"""
    query: str
    research_depth: ResearchDepth = ResearchDepth.STANDARD
    date_range_start: Optional[int] = None
    date_range_end: Optional[int] = None


class ResearchResponse(BaseModel):
    """Response model for research session"""
    session_id: str
    status: ResearchStatus
    message: str


@router.post("/start", response_model=ResearchResponse)
async def start_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new research session
    """
    from app.agents.researcher import run_research
    
    # Create research session
    session_id = str(uuid.uuid4())
    session = ResearchSession(
        id=session_id,
        user_query=request.query,
        research_depth=request.research_depth,
        status=ResearchStatus.PENDING
    )
    
    research_sessions[session_id] = session
    
    # Run research in background
    background_tasks.add_task(run_research, session_id, request.query)
    
    return ResearchResponse(
        session_id=session_id,
        status=session.status,
        message="Research session created successfully"
    )


@router.get("/{session_id}")
async def get_research_session(session_id: str):
    """
    Get research session details including reasoning process
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    
    # Include research plan if available
    plan = []
    if hasattr(session, '_research_plan'):
        plan = session._research_plan
    
    # Include reasoning steps
    reasoning = []
    if hasattr(session, '_reasoning'):
        reasoning = session._reasoning
    
    return {
        "id": session.id,
        "user_query": session.user_query,
        "research_goal": session.research_goal,
        "research_depth": session.research_depth,
        "status": session.status,
        "current_task": session.current_task,
        "progress": session.progress,
        "research_plan": plan,
        "reasoning": reasoning,
        "created_at": session.created_at,
        "completed_at": session.completed_at
    }


@router.get("/{session_id}/status")
async def get_research_status(session_id: str):
    """
    Get current status of a research session
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    return {
        "session_id": session_id,
        "status": session.status,
        "current_task": session.current_task,
        "progress": session.progress
    }


@router.get("/{session_id}/sources")
async def get_research_sources(session_id: str):
    """
    Get sources collected during research with evidence
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    
    # Get sources from session if available
    sources = []
    if hasattr(session, '_sources'):
        evidence_map = {}
        if hasattr(session, '_evidence'):
            evidence_map = session._evidence
        
        sources = [
            {
                "id": i + 1,
                "title": s.title,
                "url": s.url,
                "snippet": s.abstract,
                "type": s.source_type,
                "relevance_score": s.relevance_score,
                "evidence": evidence_map.get(i + 1, [])
            }
            for i, s in enumerate(session._sources)
        ]
    
    return {
        "session_id": session_id,
        "sources": sources,
        "count": len(sources)
    }


@router.get("/{session_id}/download/pdf")
async def download_pdf_report(session_id: str):
    """
    Download PDF report for a research session
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    
    if session.status != ResearchStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Research is not yet completed"
        )
    
    try:
        from app.services.pdf_generator import pdf_generator
        from app.tools.image_search import image_search_tool
        
        # Get session data
        query = session.user_query
        answer = session.research_goal or "No answer generated"
        
        # Get sources
        sources = []
        if hasattr(session, '_sources') and hasattr(session, '_evidence'):
            evidence_map = session._evidence
            sources = [
                {
                    "id": i + 1,
                    "title": s.title,
                    "url": s.url,
                    "evidence": evidence_map.get(i + 1, [])
                }
                for i, s in enumerate(session._sources)
            ]
        
        # Get research plan
        research_plan = []
        if hasattr(session, '_research_plan'):
            research_plan = session._research_plan
        
        # Search and download images
        image_paths = await image_search_tool.search_and_download(
            query=query,
            session_id=session_id,
            max_images=3
        )
        
        # Generate PDF
        pdf_path = pdf_generator.generate_report(
            session_id=session_id,
            query=query,
            answer=answer,
            sources=sources,
            research_plan=research_plan,
            image_paths=image_paths
        )
        
        # Check if file exists
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="PDF generation failed")
        
        # Return file
        return FileResponse(
            path=pdf_path,
            media_type='application/pdf',
            filename=f"research_report_{session_id[:8]}.pdf"
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


@router.get("/")
async def list_research_sessions():
    """
    List all research sessions
    """
    return {
        "sessions": list(research_sessions.values()),
        "count": len(research_sessions)
    }
