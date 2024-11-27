import re
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_groq import ChatGroq
from state import ResearchState

class UseCaseGeneratorTool(BaseTool):
    name: str = "use_case_generator"
    description: str = "Generate AI/ML use cases based on research"

    def __init__(self, llm: ChatGroq):
        super().__init__()
        self._llm = llm

    def _run(self, state: ResearchState) -> ResearchState:
        # Build the context from web search results
        web_context = "\n\n".join([
            f"Source: {result['title']}\nInsight: {result['content']}"
            for result in sorted(state['web_search_results'], key=lambda x: x['relevance_score'], reverse=True)[:5]
        ])

        prompt = f"""
        Generate 3-5 innovative AI/ML use cases for {state['company_name']} in {state['industry']}.

        Context:
        {web_context}

        Market Trends:
        {', '.join(state['market_trends'])}

        Company Offerings:
        {', '.join(state['key_offerings'])}

        For each use case, include:
        1. A title for the use case.
        2. An objective or purpose of the use case.
        3. How AI will be applied to achieve the objective.
        4. Cross-functional benefits, highlighting specific areas like Operations, Finance, and others.
        5. Reference links to articles used (using [number] format).

        Write the use cases in a structured narrative format like this example:
        
        Use Case 1: AI-Powered Predictive Maintenance
        Objective/Use Case: Reduce equipment downtime and maintenance costs by predicting equipment failures before they occur.
        AI Application: Implement machine learning algorithms that analyze real-time sensor data from machinery to predict potential failures and schedule maintenance proactively.
        Cross-Functional Benefits:
        - Operations & Maintenance: Minimizes unplanned downtime and extends equipment lifespan.
        - Finance: Reduces maintenance costs and improves budgeting accuracy.
        - Supply Chain: Optimizes spare parts inventory based on predictive insights.
        Articles: [1] example.com/article1, [2] example.com/article2
        """

        system_message = SystemMessage(content="""
        You are an expert AI assistant specialized in generating innovative AI/ML use cases tailored to companies' industries and market trends. Your responses should be structured, clear, and actionable, following the provided example. For each use case, make sure to include reference links to articles in [number] format at the end.
        """)

        human_message = HumanMessage(content=prompt)
        response = self._llm.invoke([system_message, human_message])

        use_cases = []
        all_articles = []
        print(response)
        
        try:
            # Split the response into individual use cases
            case_sections = re.split(r'Use Case \d+:', response.content)[1:]  # Skip empty first element
            
            for i, section in enumerate(case_sections, 1):
                # Clean up the section
                section = section.strip()
                
                # Extract all components using a single regex pattern
                patterns = {
                    'case': (r'^(.*?)(?=\nObjective/Use Case:|\n|$)', f"Use Case {i}: "),
                    'objective': (r"Objective/Use Case:\s*(.*?)(?=\n\**AI Application:|$)", ""),
                    'ai_application': (r"AI Application:\s*(.*?)(?=\n\**Cross-Functional Benefits:|$)", ""),
                    'benefits': (r"Cross-Functional Benefits:\s*(.*?)(?=\n\**Articles:|$)", []),
                    'articles': (r"Articles:\s*(.*?)(?=\n\n|$)", [])
                }
                
                # Initialize the use case dictionary
                use_case = {}
                
                # Extract each component
                for key, (pattern, default) in patterns.items():
                    match = re.search(pattern, section, re.DOTALL)
                    if match:
                        value = match.group(1).strip()
                        
                        if key == 'benefits':
                            # Process benefits list
                            benefits = [
                                benefit.strip().replace("- ", "", 1)
                                for benefit in value.split('\n')
                                if benefit.strip() and not benefit.strip().startswith("Cross-Functional Benefits:")
                            ]
                            use_case['cross_functional_benefit'] = benefits
                        elif key == 'articles':
                            # Extract URLs from [number] format
                            articles = re.findall(r'\[\d+\]\s*([^\s,]+)', value)
                            use_case['articles'] = articles
                            all_articles.extend(articles)
                        else:
                            use_case[key] = value
                    else:
                        # Use default value if pattern not found
                        use_case[key if key != 'benefits' else 'cross_functional_benefit'] = default

                use_cases.append(use_case)

        except Exception as e:
            state['errors'].append(f"Error parsing use cases: {str(e)}")
            state['use_cases'] = []
            return state

        # Update state with use cases and resource links
        state['use_cases'] = use_cases
        print(state['use_cases'])
        state['resource_links'] = list(set(all_articles))  # Remove duplicates

        return state