"""
Research planner - breaks queries into sub-questions
"""
import httpx
import json
from typing import List
from app.config import settings


async def create_research_plan(query: str) -> List[str]:
    """
    Generate a research plan with sub-questions
    
    Args:
        query: Main research query
        
    Returns:
        List of sub-questions to research
    """
    prompt = f"""You are a research planning assistant. Break down the following research question into 3-5 specific sub-questions that need to be answered.

Research Question: {query}

Provide ONLY the sub-questions, one per line, numbered. Be specific and focused.

Example format:
1. What is the definition and core concept?
2. What are the main applications?
3. What are current developments?

Sub-questions:"""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.llm_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 500
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()["response"]
                
                # Parse sub-questions from response
                sub_questions = []
                lines = result.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    # Match numbered lines like "1." or "1)"
                    if line and (line[0].isdigit() or line.startswith('-')):
                        # Remove numbering
                        question = line.split('.', 1)[-1].split(')', 1)[-1].strip()
                        if question and len(question) > 10:
                            sub_questions.append(question)
                
                # Ensure we have at least 3 questions
                if len(sub_questions) < 3:
                    sub_questions = [
                        f"What is {query}?",
                        f"What are the key aspects of {query}?",
                        f"What are current developments in {query}?"
                    ]
                
                return sub_questions[:5]  # Max 5 questions
                
    except Exception as e:
        print(f"Planning error: {e}")
        # Fallback plan
        return [
            f"What is {query}?",
            f"What are the main aspects of {query}?",
            f"What are recent developments in {query}?"
        ]
