import sys
import phi
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.groq import Groq as GroqModel

st.write(f"Python version: {sys.version}")
st.write(f"Phi version: {phi.__version__}")

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
        self.groq_model = GroqModel(
            id="llama-3.3-70b-versatile", 
            api_key=groq_api_key,
            max_tokens=4000  # Increased token limit
        )
        self.setup_agents()

    def setup_agents(self):
        # Comprehensive News Collector
        self.news_collector = Agent(
            name="Global Trend Scout",
            role="Gather comprehensive insights across multiple sources",
            tools=[DuckDuckGo(search=True, news=True, fixed_max_results=7)],
            model=self.groq_model,
            instructions=[
                "Collect diverse and recent news articles",
                "Focus on emerging trends and breakthrough innovations",
                "Provide global and regional perspectives",
                "Highlight potential disruptive technologies"
            ]
        )

        # Advanced Trend Analyzer
        self.trend_analyzer = Agent(
            name="Strategic Trend Interpreter",
            role="Deep-dive analysis of technological and market trends",
            model=self.groq_model,
            instructions=[
                "Analyze technological potential",
                "Assess market readiness and investment landscape",
                "Identify potential startup opportunities",
                "Provide actionable insights for entrepreneurs"
            ]
        )

    def generate_comprehensive_analysis(self, domains):
        analysis_results = {}
        
        for domain in domains:
            # Collect News and Insights
            news_response = self.news_collector.run(
                f"Gather latest breakthrough news and trends in {domain} "
                "focusing on startup opportunities, technological innovations, "
                "and market potential"
            )

            # Analyze Trends
            trend_response = self.trend_analyzer.run(
                f"Provide a comprehensive analysis of startup trends in {domain}. "
                "Break down technological innovations, market potential, "
                "investment landscape, and potential disruptive technologies. "
                f"Context: {news_response.content}"
            )

            analysis_results[domain] = {
                'news': news_response.content,
                'trends': trend_response.content
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
                        st.write("🌐 Market Trends:")
                        st.write(analysis_results[domain]['trends'])
                        
                        # Optional: Downloadable detailed report
                        st.download_button(
                            label=f"Download {domain} Report",
                            data=analysis_results[domain]['trends'],
                            file_name=f"{domain.replace(' ', '_')}_startup_trends.txt",
                            mime="text/plain"
                        )

        except Exception as e:
            st.error(f"Analysis failed: {e}")
    else:
        st.warning("Please select domains and enter API key")

# Footer with information
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 This platform provides data-driven insights "
    "to help entrepreneurs identify promising startup opportunities "
    "across various technological domains."
)
