"""
Research agent using LangGraph agentic workflow
"""
import asyncio
from datetime import datetime
from app.config import settings
from app.agents.agent_graph import create_research_graph

# Global storage
from app.api.research import research_sessions
from app.models.research import ResearchStatus, Source, SourceType


async def run_research(session_id: str, query: str):
    """Run the agentic research process using LangGraph"""
    session = research_sessions[session_id]
    
    try:
        # Initialize graph
        session.status = ResearchStatus.PLANNING
        session.current_task = "Initializing agentic research workflow..."
        session.progress = 5
        
        # Create initial state
        initial_state = {
            'query': query,
            'research_plan': [],
            'current_iteration': 0,
            'max_iterations': 2,  # Limit to 2 iterations max
            'sources': [],
            'evidence': [],
            'evaluation': '',
            'needs_more_research': True,
            'final_answer': '',
            'reasoning': []
        }
        
        # Create and run graph with recursion limit
        graph = create_research_graph()
        
        # Configure recursion limit
        config = {"recursion_limit": 15}
        
        # Update progress during execution
        session.current_task = "Creating research plan..."
        session.progress = 10
        await asyncio.sleep(0.3)
        
        session.status = ResearchStatus.RESEARCHING
        session.current_task = "Conducting initial research..."
        session.progress = 30
        
        # Execute graph with config
        final_state = await graph.ainvoke(initial_state, config=config)
        
        # Update with results
        session.status = ResearchStatus.ANALYZING
        session.current_task = "Analyzing and evaluating findings..."
        session.progress = 70
        await asyncio.sleep(0.3)
        
        session.status = ResearchStatus.SYNTHESIZING
        session.current_task = "Synthesizing comprehensive answer..."
        session.progress = 85
        await asyncio.sleep(0.3)
        
        # Store results
        session.status = ResearchStatus.COMPLETED
        session.current_task = "Research completed"
        session.progress = 100
        session.completed_at = datetime.utcnow()
        
        # Store answer
        session.research_goal = final_state.get('final_answer', 'No answer generated')
        
        # Store research plan
        if not hasattr(session, '_research_plan'):
            session._research_plan = final_state.get('research_plan', [])
        
        # Store sources
        sources_data = final_state.get('sources', [])
        all_sources = []
        evidence_map = {}
        
        for idx, src_data in enumerate(sources_data):
            source = Source(
                id=f"{session_id}_source_{idx}",
                session_id=session_id,
                title=src_data['title'],
                url=src_data['url'],
                source_type=SourceType.WEB,
                abstract=src_data['snippet'],
                relevance_score=1.0 - (idx * 0.03)
            )
            all_sources.append(source)
            evidence_map[src_data['id']] = src_data.get('evidence', [])
        
        if not hasattr(session, '_sources'):
            session._sources = []
        session._sources = all_sources
        
        if not hasattr(session, '_evidence'):
            session._evidence = {}
        session._evidence = evidence_map
        
        # Store reasoning
        if not hasattr(session, '_reasoning'):
            session._reasoning = []
        session._reasoning = final_state.get('reasoning', [])
        
    except Exception as e:
        session.status = ResearchStatus.FAILED
        session.current_task = f"Error: {str(e)}"
        session.progress = 0
        import traceback
        traceback.print_exc()

