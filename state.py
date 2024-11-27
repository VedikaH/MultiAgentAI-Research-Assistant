from typing import Any, Dict, List, TypedDict
from pydantic import BaseModel, Field

class UseCase(BaseModel):
    case: str = Field(description="Numbered use case")
    objective: str = Field(description="Objective or use case")
    ai_application: str = Field(description="AI application and method")
    cross_functional_benefit: List[str] = Field(description="Cross-functional benefits, broken down by areas")
    articles: List[str] = Field(description="Links of articles used")

class ResearchState(TypedDict):
    company_name: str
    industry: str
    key_offerings: List[str]
    market_trends: List[str]
    industry_insights: str
    web_search_results: List[Dict[str, Any]]
    use_cases: List[Dict[str, Any]]
    resource_links: List[str]
    errors: List[str] 