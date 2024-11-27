from pydantic import BaseModel, Field
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from tavily import TavilyClient


class WebSearchInput(BaseModel):
    query: str = Field(description="Search query string")
    max_results: int = Field(default=5, description="Maximum number of search results to return")


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Perform web search using Tavily API"
    args_schema: type[BaseModel] = WebSearchInput
    
    def __init__(self, tavily_api_key: str):
        super().__init__()
        self._tavily_client = TavilyClient(api_key=tavily_api_key)
    
    def _run(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        try:
            search_results = self._tavily_client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                include_raw_content=True
            )
            
            results = []
            for result in search_results.get('results', []):
                if isinstance(result, dict):  # Verify result is a dictionary
                    results.append({
                        'title': result.get('title', 'No Title'),
                        'url': result.get('url', ''),
                        'content': result.get('raw_content', '')[:500] + '...' if result.get('raw_content') else '',
                        'relevance_score': float(result.get('score', 0))
                    })
            
            return results if results else [{"title": "No results found", "url": "", "content": "", "relevance_score": 0}]
            
        except Exception as e:
            print(f"Web search error: {str(e)}")
            return [{"title": "Search Error", "url": "", "content": f"Web search failed: {str(e)}", "relevance_score": 0}]
