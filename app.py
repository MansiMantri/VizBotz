# import streamlit as st
# import altair as alt
# from data_processing import Process_data
# from dotenv import load_dotenv
# import json
# import os
# import pandas as pd

# # Page Config
# st.set_page_config(page_title="VizBotz - Data Visualizer", page_icon="📊", layout="wide")

# # Load .env
# load_dotenv()

# # ---------- SIDEBAR ----------
# st.sidebar.title("📊 VizBotz")

# uploaded_file = None
# columns = []
# generate_insights = False

# with st.sidebar.expander("📁 Upload Data", expanded=True):
#     uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# with st.sidebar.expander("⚙️ AI Insight Settings", expanded=True):
#     generate_insights = st.checkbox("Generate AI Insights", value=True)

# # ---------- MAIN ----------
# st.title("🚀 Interactive Data Visualizer")
# st.markdown("Upload your CSV, configure chart settings below, and generate AI-powered insights!")

# if uploaded_file:
#     try:
#         data_processor = Process_data(uploaded_file)
#         df = data_processor.get_df()

#         st.success(f"✅ Uploaded: {uploaded_file.name}")
#         st.info(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns")
#         st.markdown("---")

#         with st.expander("🔍 Preview Data", expanded=True):
#             st.dataframe(df.head(50), use_container_width=True)

#         with st.expander("📊 Descriptive Statistics"):
#             st.write(data_processor.describe_data())

#         st.markdown("---")
#         st.header("📈 Configure Visualization")

#         chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Scatter Plot", "Line Chart", "Histogram", "Pie Chart", "Box Plot"])
#         columns = df.columns.tolist()

#         x_column = st.selectbox("Select X-axis Column", columns)
#         y_column = None
#         color_column = None

#         if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]:
#             y_column = st.selectbox("Select Y-axis Column", columns)

#         if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart"]:
#             if st.checkbox("Add Color Differentiation"):
#                 color_column = st.selectbox("Select Color Column", columns)

#         chart_type_map = {
#             "Bar Chart": "bar",
#             "Scatter Plot": "point",
#             "Line Chart": "line",
#             "Histogram": "bar",
#             "Pie Chart": "arc",
#             "Box Plot": "boxplot"
#         }

#         st.markdown("---")
#         generate_clicked = st.button("🚀 Generate")

#         if generate_clicked:
#             st.subheader("📊 Visualization")

#             try:
#                 vega_spec = data_processor.generate_vegalite_spec(
#                     chart_type=chart_type_map[chart_type],
#                     x_column=x_column,
#                     y_column=y_column,
#                     color_column=color_column,
#                     insights=None
#                 )
#                 st.vega_lite_chart(vega_spec, use_container_width=True)
#             except Exception as e:
#                 st.error(f"❌ Error generating Vega chart: {e}")

#             st.markdown("---")
#             st.header("🧠 AI Insights")

#             insights = None
#             if generate_insights:
#                 with st.spinner("Generating AI insights..."):
#                     try:
#                         insights = data_processor.generate_insights_from_vega(
#                             vega_spec,
#                             x_column=x_column,
#                             y_column=y_column
#                         )

#                         if isinstance(insights, dict):
#                             if "key_observations" in insights:
#                                 st.subheader("🔑 Key Observations")
#                                 for obs in insights["key_observations"]:
#                                     st.markdown(f"• {obs}")

#                             if "trends_or_patterns" in insights:
#                                 st.subheader("📈 Trends or Patterns")
#                                 st.markdown(insights["trends_or_patterns"])

#                             if "anomalies_or_outliers" in insights:
#                                 st.subheader("🚨 Anomalies or Outliers")
#                                 st.markdown(insights["anomalies_or_outliers"])

#                             if "recommendations" in insights:
#                                 st.subheader("💡 Recommendations")
#                                 recs = insights["recommendations"]
#                                 if isinstance(recs, list):
#                                     for rec in recs:
#                                         st.markdown(f"• {rec}")
#                                 elif isinstance(recs, str):
#                                     st.markdown(recs)

#                             if "summary" in insights:
#                                 st.subheader("📝 Executive Summary")
#                                 summ = insights["summary"]
#                                 if isinstance(summ, list):
#                                     for s in summ:
#                                         st.markdown(f"• {s}")
#                                 elif isinstance(summ, str):
#                                     st.markdown(summ)

#                             st.download_button(
#                                 label="⬇️ Download AI Insights",
#                                 data=json.dumps(insights, indent=2),
#                                 file_name="ai_insights.json",
#                                 mime="application/json"
#                             )

#                     except Exception as e:
#                         st.error(f"❌ Error generating insights: {str(e)}")

#     except Exception as e:
#         st.error(f"❌ Error processing uploaded file: {str(e)}")
# else:
#     st.info("📥 Please upload a CSV file to get started!")
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

        # Smart Column Separation
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Scatter Plot", "Line Chart", "Histogram", "Pie Chart", "Box Plot"])

        st.markdown("### 📈 Configure Axes")

        # Smart X-axis selection
        if chart_type in ["Bar Chart", "Pie Chart", "Box Plot"]:
            x_column = st.selectbox("Select X-axis Column (Category)", categorical_cols)
        else:
            x_column = st.selectbox("Select X-axis Column (Numeric)", numeric_cols)

        # Smart Y-axis selection
        y_column = None
        if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]:
            y_column = st.selectbox("Select Y-axis Column (Numeric)", numeric_cols)

        # Optional color
        color_column = None
        if chart_type in ["Bar Chart", "Scatter Plot", "Line Chart"]:
            if st.checkbox("Add Color Differentiation"):
                color_column = st.selectbox("Select Color Column", categorical_cols)

        # Mapping
        chart_type_map = {
            "Bar Chart": "bar",
            "Scatter Plot": "point",
            "Line Chart": "line",
            "Histogram": "bar",
            "Pie Chart": "arc",
            "Box Plot": "boxplot"
        }

        st.markdown("---")
        generate_clicked = st.button("🚀 Generate")

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
