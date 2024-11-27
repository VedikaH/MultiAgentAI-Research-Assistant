from typing import Callable
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from Tools.industryResearchTool import IndustryResearchTool
from Tools.resourceCollectorTool import ResourceCollectorTool
from state import ResearchState
from Tools.useCaseGeneratorTool import UseCaseGeneratorTool
from Tools.webSearchTool import WebSearchTool

def create_research_workflow(groq_api_key: str, tavily_api_key: str) -> Callable:
    """Create the research workflow with tools"""
    
    # Initialize LLM with Groq's Llama 3
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",  # Using Llama 3 70B model
        temperature=0.3,
        api_key=groq_api_key
    )
    
    # Initialize tools
    web_search_tool = WebSearchTool(tavily_api_key)
    industry_research_tool = IndustryResearchTool(llm, web_search_tool)
    use_case_generator_tool = UseCaseGeneratorTool(llm)
    resource_collector_tool = ResourceCollectorTool(web_search_tool)
    
    # Create workflow
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("industry_research", industry_research_tool._run)
    workflow.add_node("use_case_generation", use_case_generator_tool._run)
    workflow.add_node("resource_collection", resource_collector_tool._run)
    
    # Define workflow
    workflow.set_entry_point("industry_research")
    workflow.add_edge("industry_research", "use_case_generation")
    workflow.add_edge("use_case_generation", "resource_collection")
    workflow.add_edge("resource_collection", END)
    
    return workflow.compile()