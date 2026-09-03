# Import asyncio at the top
import asyncio
import httpx
from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
import operator

from app.config import settings
from app.tools.web_search import search_tool
from app.agents.planner import create_research_plan
from app.services.evidence_extractor import extract_evidence, generate_cited_answer


class ResearchGraphState(TypedDict):
    """State for research graph"""
    query: str
    research_plan: List[str]
    current_iteration: int
    max_iterations: int
    sources: List[Dict]
    evidence: List[Dict]
    evaluation: str
    needs_more_research: bool
    final_answer: str
    reasoning: Annotated[List[str], operator.add]


async def plan_research(state: ResearchGraphState) -> ResearchGraphState:
    """Create research plan"""
    query = state['query']
    
    state['reasoning'].append("🧠 Research Planner: Breaking down query into sub-questions")
    
    # Generate sub-questions
    sub_questions = await create_research_plan(query)
    
    state['research_plan'] = sub_questions
    state['reasoning'].append(f"  → Created {len(sub_questions)} research questions")
    
    return state


async def conduct_research(state: ResearchGraphState) -> ResearchGraphState:
    """Execute research for current plan"""
    sources_with_evidence = []
    
    state['reasoning'].append(f"🔍 Web Search: Searching for answers using DuckDuckGo")
    
    for idx, sub_q in enumerate(state['research_plan'], 1):
        # Search for this sub-question
        search_results = await asyncio.to_thread(
            search_tool.search,
            sub_q,
            max_results=2
        )
        
        # Extract evidence from each source
        for result in search_results:
            evidence = await extract_evidence(
                result['title'],
                result['snippet'],
                result['url'],
                sub_q
            )
            
            sources_with_evidence.append({
                'id': len(sources_with_evidence) + 1,
                'title': result['title'],
                'url': result['url'],
                'snippet': result['snippet'],
                'evidence': evidence
            })
    
    state['sources'].extend(sources_with_evidence)
    state['reasoning'].append(f"  → Found {len(state['sources'])} sources with evidence")
    
    return state


async def evaluate_research(state: ResearchGraphState) -> ResearchGraphState:
    """Evaluate if we have enough information"""
    query = state['query']
    sources_count = len(state['sources'])
    
    # Increment iteration first
    state['current_iteration'] += 1
    
    state['reasoning'].append(f"🎯 Quality Check: Evaluating {sources_count} sources (Iteration {state['current_iteration']}/{state['max_iterations']})")
    
    # Auto-approve if we have enough sources or reached max iterations
    if sources_count >= 6 or state['current_iteration'] >= state['max_iterations']:
        state['evaluation'] = "SUFFICIENT"
        state['needs_more_research'] = False
        state['reasoning'].append(f"  → Quality: SUFFICIENT - Ready to synthesize answer")
        return state
    
    # Build evaluation prompt
    evidence_summary = "\n".join([
        f"- {s['title']}: {len(s.get('evidence', []))} facts"
        for s in state['sources'][:10]
    ])
    
    prompt = f"""You are evaluating research quality. 

Question: {query}
Sources found: {sources_count}
Evidence collected:
{evidence_summary}

Evaluate if we have SUFFICIENT information to answer the question comprehensively.

Respond with ONLY one word:
- "SUFFICIENT" if we have enough quality information
- "INSUFFICIENT" if we need more research

Evaluation:"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 50
                    }
                }
            )
            
            if response.status_code == 200:
                evaluation = response.json()["response"].strip().upper()
                
                # Check if we need more research
                needs_more = "INSUFFICIENT" in evaluation and state['current_iteration'] < state['max_iterations']
                
                state['evaluation'] = evaluation
                state['needs_more_research'] = needs_more
                state['reasoning'].append(f"  → Quality: {evaluation} - {'Need more sources' if needs_more else 'Ready to synthesize'}")
                
    except Exception as e:
        print(f"Evaluation error: {e}")
        state['needs_more_research'] = False
        state['evaluation'] = "SUFFICIENT (error fallback)"
        state['reasoning'].append(f"  → Proceeding to synthesis")
    
    return state


async def synthesize_answer(state: ResearchGraphState) -> ResearchGraphState:
    """Generate final answer with citations"""
    state['reasoning'].append(f"📝 Answer Generator: Creating comprehensive answer with citations")
    
    cited_answer = await generate_cited_answer(
        state['query'],
        state['sources']
    )
    
    state['final_answer'] = cited_answer
    state['reasoning'].append(f"  → Generated answer with [1][2][3] style citations from {len(state['sources'])} sources")
    
    return state


def should_continue_research(state: ResearchGraphState) -> str:
    """Decision: continue research or finalize"""
    # Always finalize if we've reached max iterations
    if state['current_iteration'] >= state['max_iterations']:
        return "finalize"
    
    # Finalize if we don't need more research
    if not state.get('needs_more_research', False):
        return "finalize"
    
    # Continue if we need more and haven't hit limit
    return "research_more"


async def research_more(state: ResearchGraphState) -> ResearchGraphState:
    """Generate additional research queries based on gaps"""
    query = state['query']  # Get query from state
    
    state['reasoning'].append(f"🔄 Gap Analysis: Identifying missing information")
    
    prompt = f"""Based on the research so far, suggest 2 additional specific questions to fill information gaps.

Original Question: {query}
Already researched: {len(state['sources'])} sources

Provide 2 NEW specific questions that would add valuable information:"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 200
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()["response"]
                
                # Parse additional questions
                additional_questions = []
                lines = result.strip().split('\n')
                for line in lines:
                    line = line.strip().lstrip('123456789.-) ')
                    if line and len(line) > 10:
                        additional_questions.append(line)
                
                state['research_plan'] = additional_questions[:2]
                state['reasoning'].append(f"  → Found gaps, researching {len(additional_questions[:2])} more angles")
                
    except Exception as e:
        print(f"Research more error: {e}")
        state['needs_more_research'] = False
        state['reasoning'].append(f"  → Proceeding with current research")
    
    return state


# Create the graph
def create_research_graph():
    """Build the LangGraph research workflow"""
    workflow = StateGraph(ResearchGraphState)
    
    # Add nodes
    workflow.add_node("plan", plan_research)
    workflow.add_node("research", conduct_research)
    workflow.add_node("evaluate", evaluate_research)
    workflow.add_node("research_more", research_more)
    workflow.add_node("synthesize", synthesize_answer)
    
    # Define edges
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "research")
    workflow.add_edge("research", "evaluate")
    
    # Conditional edge based on evaluation
    workflow.add_conditional_edges(
        "evaluate",
        should_continue_research,
        {
            "research_more": "research_more",
            "finalize": "synthesize"
        }
    )
    
    # Loop back to research after generating more questions
    workflow.add_edge("research_more", "research")
    workflow.add_edge("synthesize", END)
    
    return workflow.compile()
