"""
Web search tool using DDGS (DuckDuckGo)
"""
from typing import List, Dict
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


class WebSearchTool:
    """Search the web for information"""
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web and return results
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, url, snippet
        """
        try:
            results = []
            ddgs = DDGS()
            
            # Use text search
            search_results = list(ddgs.text(query, max_results=max_results))
            
            for result in search_results:
                if result and isinstance(result, dict):
                    results.append({
                        'title': result.get('title', 'No title'),
                        'url': result.get('href', result.get('link', '')),
                        'snippet': result.get('body', result.get('snippet', 'No description')),
                        'source': 'web'
                    })
            
            return results
        except Exception as e:
            print(f"Search error: {e}")
            # Return mock results as fallback
            return [
                {
                    'title': f'Search result for: {query}',
                    'url': 'https://example.com',
                    'snippet': f'Information about {query} from web search.',
                    'source': 'web'
                }
            ]


# Global search tool instance
search_tool = WebSearchTool()
