import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# LangChain Imports
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.tools import DuckDuckGoSearchResults

class ComprehensiveStartupTrendAnalyzer:
    STARTUP_DOMAINS = [
        'AI/Machine Learning', 'Biotechnology', 'CleanTech', 
        'FinTech', 'EdTech', 'SpaceTech', 'Cybersecurity', 
        'Robotics', 'Healthcare Tech', 'AgriTech', 
        'Quantum Computing', 'Blockchain/Web3', 
        'Renewable Energy', 'Climate Tech', 
        'Advanced Materials', 'Autonomous Vehicles'
    ]

    def __init__(self, groq_api_key):
        # Initialize LangChain Groq Chat Model
        self.llm = ChatGroq(
            temperature=0.2, 
            model_name="llama-3-70b-8192",
            groq_api_key=groq_api_key
        )
        
        # Initialize Search Tool
        self.search_tool = DuckDuckGoSearchResults()

    def generate_comprehensive_analysis(self, domains):
        analysis_results = {}
        
        for domain in domains:
            # Search for recent news and trends
            search_results = self.search_tool.run(f"Latest startup trends in {domain} 2024")
            
            # Create a prompt for trend analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert startup trend analyst. 
                Provide a comprehensive analysis of startup trends based on the following context.
                Focus on:
                - Technological innovations
                - Market potential
                - Investment landscape
                - Emerging opportunities
                
                Respond in a structured JSON format with key insights."""),
                ("human", """Analyze the following context about {domain} startup trends:
                Recent Search Results: {search_results}
                
                Provide a detailed analysis in the following JSON structure:
                {{
                    "domain": "{domain}",
                    "key_technologies": [],
                    "market_potential": "",
                    "investment_trends": "",
                    "emerging_opportunities": [],
                    "challenges": []
                }}""")
            ])
            
            # Create a chain with output parsing
            chain = prompt | self.llm | JsonOutputParser()
            
            try:
                # Generate analysis
                trend_response = chain.invoke({
                    "domain": domain, 
                    "search_results": search_results
                })
                
                analysis_results[domain] = trend_response
            except Exception as e:
                analysis_results[domain] = {
                    "error": f"Analysis failed for {domain}: {str(e)}"
                }
        
        return analysis_results

    def generate_trend_metrics(self, domains):
        # Simulated startup trend metrics
        metrics_data = []
        for domain in domains:
            metrics_data.append({
                'Domain': domain,
                'Market Potential': np.random.randint(50, 95),
                'Innovation Score': np.random.randint(50, 95),
                'Investment Attractiveness': np.random.randint(50, 95)
            })
        
        return pd.DataFrame(metrics_data)

    def create_visualizations(self, metrics_df):
        # Radar Chart for Trend Metrics
        radar_fig = go.Figure()
        for index, row in metrics_df.iterrows():
            radar_fig.add_trace(go.Scatterpolar(
                r=[row['Market Potential'], row['Innovation Score'], row['Investment Attractiveness']],
                theta=['Market Potential', 'Innovation Score', 'Investment Attractiveness'],
                fill='toself',
                name=row['Domain']
            ))
        
        radar_fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title='Startup Domain Trend Radar'
        )

        # Bar Chart for Comparative Analysis
        bar_fig = px.bar(
            metrics_df, 
            x='Domain', 
            y=['Market Potential', 'Innovation Score', 'Investment Attractiveness'],
            title='Startup Domains: Comparative Trend Analysis',
            barmode='group'
        )

        return radar_fig, bar_fig

# Streamlit UI
st.set_page_config(page_title="Startup Trend Intelligence", layout="wide")
st.title("🚀 Comprehensive Startup Trend Intelligence Platform")

# Sidebar for configuration
st.sidebar.header("Analysis Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

# Multi-select for domains with more options
selected_domains = st.sidebar.multiselect(
    "Select Startup Domains for Analysis", 
    ComprehensiveStartupTrendAnalyzer.STARTUP_DOMAINS,
    default=['AI/Machine Learning', 'Biotechnology', 'FinTech']
)

# Analysis depth and focus
analysis_depth = st.sidebar.slider("Analysis Depth", 1, 10, 7)
focus_areas = st.sidebar.multiselect(
    "Focus Areas",
    ['Technological Innovation', 'Market Potential', 'Investment Landscape', 'Emerging Trends']
)

if st.sidebar.button("Generate Comprehensive Analysis"):
    if groq_api_key and selected_domains:
        try:
            # Initialize Analyzer
            analyzer = ComprehensiveStartupTrendAnalyzer(groq_api_key)
            
            # Generate Comprehensive Analysis
            analysis_results = analyzer.generate_comprehensive_analysis(selected_domains)
            
            # Generate Trend Metrics
            metrics_df = analyzer.generate_trend_metrics(selected_domains)
            
            # Create Visualizations
            radar_chart, bar_chart = analyzer.create_visualizations(metrics_df)

            # Display Results
            st.header("🔍 Startup Trend Intelligence Report")
            
            # Visualizations Tab
            viz_tab, insights_tab = st.tabs(["Visual Trends", "Domain Insights"])
            
            with viz_tab:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(radar_chart, use_container_width=True)
                with col2:
                    st.plotly_chart(bar_chart, use_container_width=True)
            
            # Insights Tab
            with insights_tab:
                for domain in selected_domains:
                    with st.expander(f"{domain} - Trend Analysis"):
                        # Check if analysis was successful
                        if 'error' in analysis_results[domain]:
                            st.error(analysis_results[domain]['error'])
                        else:
                            # Display parsed insights
                            st.write("🌐 Market Trends:")
                            st.json(analysis_results[domain])
                            
                            # Optional: Downloadable detailed report
                            st.download_button(
                                label=f"Download {domain} Report",
                                data=str(analysis_results[domain]),
                                file_name=f"{domain.replace(' ', '_')}_startup_trends.json",
                                mime="application/json"
                            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")
    else:
        st.warning("Please select domains and enter API key")

# Footer with information
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 This platform provides AI-powered insights "
    "to help entrepreneurs identify promising startup opportunities "
    "across various technological domains."
)
