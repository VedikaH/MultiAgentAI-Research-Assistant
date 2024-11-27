import streamlit as st
import json
from dotenv import load_dotenv
import os
from workflow import create_research_workflow

def main():

    load_dotenv()  # Load variables from .env
    # Now you can access variables like:
    groq_api_key = os.getenv('groq_api_key')
    tavily_api_key=os.getenv('tavily_api_key')

    workflow = create_research_workflow(groq_api_key, tavily_api_key)
    
    # Test cases
    st.set_page_config(
        page_title="Company Research Tool",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Company Research Tool")
    

    
    # Main input form
    st.subheader("Enter Company Details")
    with st.form("research_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name", placeholder="e.g., Tesla")
        with col2:
            domain = st.text_input("Industry", placeholder="e.g., Automotive")
        
        submitted = st.form_submit_button("Start Research", use_container_width=True)
    
    if submitted:
        if not company_name or not domain:
            st.error("Please enter both company name and domain.")
            return
        
        # Show progress
        with st.spinner(f"Researching {company_name}..."):
            try:
                # Create workflow
                workflow = create_research_workflow(groq_api_key, tavily_api_key)
                
                # Prepare initial state
                initial_state = {
                    'company_name': company_name,
                    'industry': domain,
                }
                
                # Run workflow
                result = workflow.invoke(initial_state)
                
                # Display results in organized tabs
                st.success("Research completed!")
                
                tabs = st.tabs([
                    "Key Offerings",
                    "Market Trends",
                    "Industry Insights",
                    "Use Cases",
                    "Resources"
                ])
                
                with tabs[0]:
                    st.subheader("Key Offerings")
                    for offering in result['key_offerings']:
                        st.write(f"• {offering}")
                
                with tabs[1]:
                    st.subheader("Market Trends")
                    for trend in result['market_trends']:
                        st.write(f"• {trend}")
                
                with tabs[2]:
                    st.subheader("Industry Insights")
                    st.write(result['industry_insights'])
                    
                    st.subheader("Web Search Results")
                    for web in result['web_search_results']:
                        st.markdown(f"### {web['title']}")
                        st.markdown(f"**URL:** {web['url']}")
                        st.markdown(f"**Snippet:** {web['content'][:700]}...")  # Display a preview of the content
                        st.markdown(f"**Relevance Score:** {web['relevance_score']:.2f}")
                        st.markdown("---")
                
                with tabs[3]:
                    st.subheader("Use Cases")
                    for use_case in result['use_cases']:
                        st.markdown(f"### {use_case['case']}")
                        st.markdown(f"**Objective:** {use_case['objective']}")
                        st.markdown(f"**AI Application:** {use_case['ai_application']}")
                        st.markdown("**Cross-Functional Benefits:**")
                        for benefit in use_case['cross_functional_benefit']:
                            st.write(f"- {benefit}")
                        st.markdown("**Related Articles:**")
                        for article in use_case['articles']:
                            st.markdown(f"- [Read more here]({article})")
                        st.markdown("---")  # Adds a horizontal line for separation
                
                with tabs[4]:
                    st.subheader("Resource Links")
                    for link in result['resource_links']:
                        st.write(f"• [{link}]({link})")
                
            except Exception as e:
                st.error(f"Error during research: {str(e)}")

if __name__ == "__main__":
    main()