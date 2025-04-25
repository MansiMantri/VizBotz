# import streamlit as st
# import plotly.express as px
# import altair as alt
# from data_processing import Process_data
# import json
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Set page configuration
# st.set_page_config(
#     page_title="Data Visualizer",
#     page_icon="📊",
#     layout="wide"
# )

# # Add title and description
# st.title("Interactive Data Visualizer")
# st.markdown("Upload your CSV file and create interactive visualizations with AI-powered insights!")

# # Sidebar for file upload and options
# with st.sidebar:
#     st.header("Upload Data")
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
#     if uploaded_file is not None:
#         # Initialize data processor
#         data_processor = Process_data(uploaded_file)
#         df = data_processor.get_df()
        
#         # Display data info
#         st.header("Data Information")
#         st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
#         # Visualization options
#         st.header("Visualization Options")
#         viz_type = st.selectbox(
#             "Select Visualization Type",
#             ["Bar Chart", "Scatter Plot", "Line Chart", "Histogram", "Pie Chart", "Box Plot"]
#         )
        
#         # Get column names
#         columns = data_processor.get_columns()
        
#         # Common options
#         x_column = st.selectbox("Select X-axis Column", columns)
        
#         # Y-axis for applicable charts
#         if viz_type in ["Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]:
#             y_column = st.selectbox("Select Y-axis Column", columns)
#         else:
#             y_column = None
            
#         # Color option for applicable charts
#         if viz_type in ["Bar Chart", "Scatter Plot", "Line Chart"]:
#             color_option = st.checkbox("Add Color Differentiation")
#             if color_option:
#                 color_column = st.selectbox("Select Color Column", columns)
#             else:
#                 color_column = None
#         else:
#             color_column = None
            
#         # Generate insights option
#         generate_insights = st.checkbox("Generate AI Insights", value=True)
        
#         # Visualization library selection
#         viz_library = st.radio("Select Visualization Library", ["Plotly", "Vega-Lite"])

# # Main content area
# if uploaded_file is not None:
#     # Show data table
#     st.header("Data Preview")
#     st.dataframe(df.head())
    
#     # Show descriptive statistics
#     with st.expander("Descriptive Statistics"):
#         st.write(data_processor.describe_data())
    
#     # Generate visualization
#     st.header("Visualization")
    
#     # Map visualization type to chart type for API
#     chart_type_map = {
#         "Bar Chart": "bar",
#         "Scatter Plot": "scatter",
#         "Line Chart": "line",
#         "Histogram": "histogram",
#         "Pie Chart": "pie",
#         "Box Plot": "box"
#     }
    
#     # Get insights if requested
#     insights = None
#     # In the sidebar, add a debug mode option
#     debug_mode = st.sidebar.checkbox("Debug Mode", value=False)
    
#     # Then in the insights generation section:
#     if generate_insights:
#         with st.spinner("Generating insights..."):
#             try:
#                 if debug_mode:
#                     st.info("Calling DeepSeek API for insights...")
                    
#                 insights = data_processor.generate_insights(
#                     chart_type=chart_type_map[viz_type].lower(),
#                     x_column=x_column,
#                     y_column=y_column,
#                     color_column=color_column
#                 )
                
#                 if debug_mode:
#                     st.success("API call completed")
#                     st.json(insights)
#             except Exception as e:
#                 st.error(f"Error generating insights: {str(e)}")
#                 if "API key" in str(e):
#                     st.info("Please set the DEEPSEEK_API_KEY in your environment variables or .env file.")
#                 elif debug_mode:
#                     st.error(f"Full error: {str(e)}")
#                 if "API key" in str(e):
#                     st.info("Please set the DEEPSEEK_API_KEY in your environment variables or .env file.")
    
#     # Create visualization based on selected library
#     if viz_library == "Plotly":
#         # Create Plotly visualization
#         if viz_type == "Bar Chart":
#             if y_column:
#                 fig = px.bar(df, x=x_column, y=y_column, color=color_column, title=f"Bar Chart: {x_column} vs {y_column}")
#             else:
#                 fig = px.bar(df, x=x_column, title=f"Bar Chart: {x_column}")
                
#         elif viz_type == "Scatter Plot":
#             fig = px.scatter(df, x=x_column, y=y_column, color=color_column, title=f"Scatter Plot: {x_column} vs {y_column}")
            
#         elif viz_type == "Line Chart":
#             fig = px.line(df, x=x_column, y=y_column, color=color_column, title=f"Line Chart: {x_column} vs {y_column}")
            
#         elif viz_type == "Histogram":
#             fig = px.histogram(df, x=x_column, title=f"Histogram: {x_column}")
            
#         elif viz_type == "Pie Chart":
#             fig = px.pie(df, names=x_column, title=f"Pie Chart: {x_column}")
            
#         elif viz_type == "Box Plot":
#             fig = px.box(df, x=x_column, y=y_column, title=f"Box Plot: {x_column} vs {y_column}")
        
#         # Display the figure
#         st.plotly_chart(fig, use_container_width=True)
        
#     else:  # Vega-Lite
#         # Generate Vega-Lite spec with insights
#         vega_spec = data_processor.generate_vegalite_spec(
#             chart_type=chart_type_map[viz_type].lower(),
#             x_column=x_column,
#             y_column=y_column,
#             color_column=color_column,
#             insights=insights
#         )
        
#         # Display Vega-Lite chart
#         st.vega_lite_chart(vega_spec)
    
#     # Inside the main content area, update the insights display section:
    
#     # Display insights separately if available
#     if insights:
#         st.header("AI-Generated Insights")
        
#         # Check if there was an error
#         if isinstance(insights, dict) and insights.get('error'):
#             st.error(f"Error generating insights: {insights.get('error')}")
#             if insights.get('raw_response'):
#                 with st.expander("Raw API Response"):
#                     st.text(insights.get('raw_response'))
#         else:
#             # Display key observations
#             if isinstance(insights, dict) and "key_observations" in insights and insights["key_observations"]:
#                 st.subheader("Key Observations")
#                 if isinstance(insights["key_observations"], list):
#                     for observation in insights["key_observations"]:
#                         st.markdown(f"• {observation}")
#                 else:
#                     st.markdown(f"• {insights['key_observations']}")
            
#             # Display trends
#             if isinstance(insights, dict) and "trends_or_patterns" in insights and insights["trends_or_patterns"]:
#                 st.subheader("Trends or Patterns")
#                 st.write(insights["trends_or_patterns"])
            
#             # Display anomalies
#             if isinstance(insights, dict) and "anomalies_or_outliers" in insights and insights["anomalies_or_outliers"]:
#                 st.subheader("Anomalies or Outliers")
#                 st.write(insights["anomalies_or_outliers"])
            
#             # Display recommendations
#             if isinstance(insights, dict) and "recommendations" in insights and insights["recommendations"]:
#                 st.subheader("Recommendations")
#                 st.write(insights["recommendations"])
            
#             # Display summary
#             if isinstance(insights, dict) and "summary" in insights and insights["summary"]:
#                 st.subheader("Summary")
#                 st.write(insights["summary"])
            
#             # If none of the expected fields are present, display whatever we got
#             if not any(k in insights for k in ["key_observations", "trends_or_patterns", "anomalies_or_outliers", "recommendations", "summary"]):
#                 st.subheader("Raw Insights")
#                 st.json(insights)
    
#     # Option to download Vega-Lite spec as JSON
#     if viz_library == "Vega-Lite":
#         st.download_button(
#             label="Download Vega-Lite Specification",
#             data=json.dumps(vega_spec, indent=2),
#             file_name="vega_lite_spec.json",
#             mime="application/json"
#         )

# else:
#     # Display instructions when no file is uploaded
#     st.info("Please upload a CSV file to get started.")
    
#     # Example section
#     st.header("How to Use")
#     st.markdown("""
#     1. Upload your CSV file using the sidebar
#     2. Select visualization type and options
#     3. Choose whether to generate AI insights
#     4. Explore your data with interactive visualizations
#     5. Download visualization specifications for reuse
#     """)
import streamlit as st
import altair as alt
from data_processing import Process_data
from dotenv import load_dotenv
import json
import os
import pandas as pd

# Page Config
st.set_page_config(page_title="VizBotz - Data Visualizer", page_icon="📊", layout="wide")

# Load .env
load_dotenv()

# ---------- SIDEBAR ----------
st.sidebar.title("📊 VizBotz")

uploaded_file = None
columns = []
generate_insights = False

with st.sidebar.expander("📁 Upload Data", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

with st.sidebar.expander("⚙️ AI Insight Settings", expanded=True):
    generate_insights = st.checkbox("Generate AI Insights", value=True)

# ---------- MAIN ----------
st.title("🚀 Interactive Data Visualizer")
st.markdown("Upload your CSV, configure chart settings below, and generate AI-powered insights!")

if uploaded_file:
    try:
        data_processor = Process_data(uploaded_file)
        df = data_processor.get_df()

        st.success(f"✅ Uploaded: {uploaded_file.name}")
        st.info(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        st.markdown("---")

        with st.expander("🔍 Preview Data", expanded=True):
            st.dataframe(df.head(50), use_container_width=True)

        with st.expander("📊 Descriptive Statistics"):
            st.write(data_processor.describe_data())

        st.markdown("---")
        st.header("📈 Configure Visualization")

        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Scatter Plot", "Line Chart", "Histogram", "Pie Chart", "Box Plot"])
        columns = df.columns.tolist()

        x_column = st.selectbox("Select X-axis Column", columns)
        y_column = None
        color_column = None

        if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]:
            y_column = st.selectbox("Select Y-axis Column", columns)

        if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart"]:
            if st.checkbox("Add Color Differentiation"):
                color_column = st.selectbox("Select Color Column", columns)

        chart_type_map = {
            "Bar Chart": "bar",
            "Scatter Plot": "point",
            "Line Chart": "line",
            "Histogram": "bar",
            "Pie Chart": "arc",
            "Box Plot": "boxplot"
        }

        st.markdown("---")
        generate_clicked = st.button("🚀 Generate Visualization & Insights")

        if generate_clicked:
            st.subheader("📊 Visualization")

            try:
                vega_spec = data_processor.generate_vegalite_spec(
                    chart_type=chart_type_map[chart_type],
                    x_column=x_column,
                    y_column=y_column,
                    color_column=color_column,
                    insights=None
                )
                st.vega_lite_chart(vega_spec, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error generating Vega chart: {e}")

            st.markdown("---")
            st.header("🧠 AI Insights")

            insights = None
            if generate_insights:
                with st.spinner("Generating AI insights..."):
                    try:
                        insights = data_processor.generate_insights_from_vega(
                            vega_spec,
                            x_column=x_column,
                            y_column=y_column
                        )

                        if isinstance(insights, dict):
                            if "key_observations" in insights:
                                st.subheader("🔑 Key Observations")
                                for obs in insights["key_observations"]:
                                    st.markdown(f"• {obs}")

                            if "trends_or_patterns" in insights:
                                st.subheader("📈 Trends or Patterns")
                                st.markdown(insights["trends_or_patterns"])

                            if "anomalies_or_outliers" in insights:
                                st.subheader("🚨 Anomalies or Outliers")
                                st.markdown(insights["anomalies_or_outliers"])

                            if "recommendations" in insights:
                                st.subheader("💡 Recommendations")
                                recs = insights["recommendations"]
                                if isinstance(recs, list):
                                    for rec in recs:
                                        st.markdown(f"• {rec}")
                                elif isinstance(recs, str):
                                    st.markdown(recs)

                            if "summary" in insights:
                                st.subheader("📝 Executive Summary")
                                summ = insights["summary"]
                                if isinstance(summ, list):
                                    for s in summ:
                                        st.markdown(f"• {s}")
                                elif isinstance(summ, str):
                                    st.markdown(summ)

                            st.download_button(
                                label="⬇️ Download AI Insights",
                                data=json.dumps(insights, indent=2),
                                file_name="ai_insights.json",
                                mime="application/json"
                            )

                    except Exception as e:
                        st.error(f"❌ Error generating insights: {str(e)}")

    except Exception as e:
        st.error(f"❌ Error processing uploaded file: {str(e)}")
else:
    st.info("📥 Please upload a CSV file to get started!")
