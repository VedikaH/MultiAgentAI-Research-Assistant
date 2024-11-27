from langchain_core.tools import BaseTool
from state import ResearchState
from Tools.webSearchTool import WebSearchTool

class ResourceCollectorTool(BaseTool):
    name: str = "resource_collector"
    description: str = "Collect relevant resources and datasets"
    
    def __init__(self, web_search_tool: WebSearchTool):
        super().__init__()
        self._web_search_tool = web_search_tool
    
    def _run(self, state: ResearchState) -> ResearchState:
        resource_searches = []
        
        # Search for each use case
        for use_case in state['use_cases']:
            query = f"Datasets and resources for {use_case['objective']} in {state['industry']}"
            results = self._web_search_tool._run(query=query, max_results=3)
            resource_searches.extend(results)
        
        # Add general industry resources
        industry_query = f"AI ML datasets resources {state['industry']} industry github kaggle"
        industry_results = self._web_search_tool._run(query=industry_query, max_results=5)
        resource_searches.extend(industry_results)
        
        # Filter and deduplicate relevant resources
        relevant_domains = [
            'kaggle.com/datasets',
            'huggingface.co/datasets',
            'github.com',
            'paperswithcode.com',
            'tensorflow.org/datasets',
            'pytorch.org/data'
        ]
        
        filtered_urls = set()
        for result in resource_searches:
            url = result.get('url', '')
            if url and any(domain in url.lower() for domain in relevant_domains):
                filtered_urls.add(url)
        
        state['resource_links'] = list(filtered_urls)
        #print("Resource",state['resource_links'] )
        return state
