import json
from typing import List
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from state import ResearchState
from Tools.webSearchTool import WebSearchTool

class IndustryResearchTool(BaseTool):
    name: str = "industry_research"
    description: str = "Conduct comprehensive industry research"
    
    def __init__(self, llm: ChatGroq, web_search_tool: WebSearchTool):
        super().__init__()
        self._llm = llm
        self._web_search_tool = web_search_tool
    
    def _discover_key_offerings(self, company_name: str, industry: str) -> List[str]:
        """Discover company's key offerings using web search and LLM analysis"""
        # Search for company information
        company_search = self._web_search_tool._run(
            query=f"{company_name} main products services offerings {industry}",
            max_results=5
        )
        
        # Prepare context for LLM
        company_context = "\n\n".join([
            f"Title: {result['title']}\nContent: {result['content']}"
            for result in company_search
        ])
        
        # Generate key offerings using LLM
        offerings_prompt = f"""
        Based on the following information about {company_name} in the {industry} industry,
        list their main products, services, and key offerings.
        
        Information:
        {company_context}
        
        Extract and list the key offerings in a JSON array format. Include only the main,
        verified offerings (typically 3-7 items). Example format:
        ["Product 1", "Service 1", "Technology 1"]
        
        Focus on current, active offerings only.
        """
        
        response = self._llm.invoke([HumanMessage(content=offerings_prompt)])
        
        try:
            # Extract JSON array from response
            content = response.content
            start_idx = content.find('[')
            end_idx = content.find(']') + 1
            if start_idx != -1 and end_idx != -1:
                offerings_json = content[start_idx:end_idx]
                offerings = json.loads(offerings_json)
                return [str(offering) for offering in offerings]
            return []
        except Exception as e:
            print(f"Error parsing key offerings: {e}")
            return []
    
    def _run(self, state: ResearchState) -> ResearchState:
        # First, discover key offerings
        key_offerings = self._discover_key_offerings(state['company_name'], state['industry'])
        state['key_offerings'] = key_offerings
        
        # Generate comprehensive search queries using discovered offerings
        queries = [
            f"Latest AI and technology trends in {state['industry']} industry",
            f"Top technological innovations for {state['company_name']} {state['industry']}",
            f"AI and machine learning applications in {state['industry']}"
        ]
        
        # Add offering-specific queries
        for offering in key_offerings:
            queries.append(f"AI technology trends {offering} in {state['industry']}")
        
        # Collect search results
        all_results = []
        for query in queries:
            results = self._web_search_tool._run(query=query,max_results=10)
            all_results.extend(results)
        
        # Prepare context for LLM
        search_context = "\n\n".join([
            f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}"
            for result in sorted(all_results, key=lambda x: x['relevance_score'], reverse=True)[:10]
        ])
        
        # Generate analysis using LLM
        analysis_prompt = f"""
        Analyze the following information for {state['company_name']} in the {state['industry']} industry.
        
        Company Key Offerings: {', '.join(key_offerings)}
        
        Web Search Results:
        {search_context}
        
        Provide a comprehensive analysis including:
        1. Detailed market trends (list format)
        2. Technological landscape overview, especially relating to their key offerings:
           {', '.join(key_offerings)}
        3. Potential AI/ML opportunities specific to their offerings
        4. Competitive insights
        5. Emerging technologies relevant to their market position
        
        Format the market trends as a clear, numbered list.
        """
        
        response = self._llm.invoke([HumanMessage(content=analysis_prompt)])
        
        # Update state
        state['market_trends'] = self._extract_trends(response.content)
        state['industry_insights'] = response.content
        state['web_search_results'] = sorted(
                                            all_results, 
                                            key=lambda x: x['relevance_score'], 
                                            reverse=True
                                        )[:10]
        # print("market_trends:",state['market_trends'])
        # print("industry_insights",state['industry_insights'] )
        # print("web_search_results",state['web_search_results'])
        
        return state
    
    def _extract_trends(self, content: str) -> List[str]:
        return [line.strip() for line in content.split('\n') 
                if line.strip() and len(line) > 10 and 
                any(c.isdigit() for c in line[:2])][:5]