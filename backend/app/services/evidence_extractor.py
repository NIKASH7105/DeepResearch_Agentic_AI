"""
Extract key evidence from sources
"""
import httpx
from typing import List, Dict
from app.config import settings


async def extract_evidence(source_title: str, source_snippet: str, source_url: str, query_context: str) -> List[str]:
    """
    Extract key evidence/facts from a source
    
    Args:
        source_title: Title of the source
        source_snippet: Text snippet from source
        source_url: URL of the source
        query_context: Research context to focus extraction
        
    Returns:
        List of key evidence points
    """
    prompt = f"""Extract 2-3 key facts or evidence points from this source that are relevant to: {query_context}

Source: {source_title}
Content: {source_snippet}

Provide ONLY the key facts, one per line, as brief statements (max 15 words each).
Format: bullet points without symbols.

Key facts:"""

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 200
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()["response"]
                
                # Parse facts
                facts = []
                lines = result.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    # Remove bullet points, numbers, dashes
                    line = line.lstrip('-•*123456789. ')
                    if line and len(line) > 10:
                        facts.append(line)
                
                return facts[:3]  # Max 3 facts per source
                
    except Exception as e:
        print(f"Evidence extraction error: {e}")
        return []


async def generate_cited_answer(query: str, sources_with_evidence: List[Dict]) -> str:
    """
    Generate answer with inline citations
    
    Args:
        query: Research query
        sources_with_evidence: List of sources with their evidence
        
    Returns:
        Answer with [1], [2] style citations
    """
    # Build context with numbered sources
    context = "Available sources with evidence:\n\n"
    
    for i, source in enumerate(sources_with_evidence, 1):
        context += f"[{i}] {source['title']}\n"
        context += f"    URL: {source['url']}\n"
        if source.get('evidence'):
            context += "    Key facts:\n"
            for fact in source['evidence']:
                context += f"    - {fact}\n"
        context += "\n"
    
    prompt = f"""You are a research assistant. Write a comprehensive answer using the sources below. 

IMPORTANT: Add citation numbers [1], [2], [3] etc. after statements to show which source supports each claim.

{context}

Research Question: {query}

Write a detailed answer that:
1. Uses information from the sources above
2. Adds [number] citations after each fact or claim
3. Is well-organized and comprehensive
4. Cites sources accurately

Answer with citations:"""

    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.5,
                        "num_predict": settings.max_tokens
                    }
                }
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
    except Exception as e:
        print(f"Answer generation error: {e}")
        return "Error generating cited answer"
