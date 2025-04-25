import pandas as pd
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

class Process_data:

    def __init__(self, data):
        self.data = pd.read_csv(data)
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

    def get_df(self):
        return self.data

    def get_columns(self):
        return self.data.columns.to_list()

    def get_bar_data(self):
        return self.data

    def get_mean(self, col_name):
        return self.data[col_name].mean()

    def describe_data(self):
        return self.data.describe()

    def generate_chart_summary(self, x_column, y_column=None, top_n=5):
        summary = {}

        if y_column:
            if self.data[y_column].dtype in ["int64", "float64"]:
                top_samples = self.data[[x_column, y_column]].sort_values(by=y_column, ascending=False).head(top_n)
                bottom_samples = self.data[[x_column, y_column]].sort_values(by=y_column, ascending=True).head(top_n)

                summary["top_samples"] = top_samples.to_dict(orient="records")
                summary["bottom_samples"] = bottom_samples.to_dict(orient="records")

                stats = self.data[y_column].describe().to_dict()
                summary["stats"] = {
                    "mean": stats.get("mean"),
                    "std_dev": stats.get("std"),
                    "min": stats.get("min"),
                    "max": stats.get("max"),
                    "count": stats.get("count")
                }
        else:
            counts = self.data[x_column].value_counts().reset_index()
            counts.columns = [x_column, "count"]

            top_samples = counts.sort_values(by="count", ascending=False).head(top_n)
            bottom_samples = counts.sort_values(by="count", ascending=True).head(top_n)

            summary["top_samples"] = top_samples.to_dict(orient="records")
            summary["bottom_samples"] = bottom_samples.to_dict(orient="records")
            summary["stats"] = {
                "total_categories": len(counts)
            }

        return summary

    def generate_insights_from_vega(self, vega_spec, x_column, y_column=None):
        try:
            summary = self.generate_chart_summary(x_column, y_column)

            prompt = f"""
You are a senior data analyst reviewing a dataset visualization.

Chart Overview:
- Chart Type: {vega_spec.get('mark', 'Unknown')}
- X-axis: {x_column}
- Y-axis: {y_column if y_column else 'N/A'}

Sample Key Data Points:
Top Samples:
{json.dumps(summary.get('top_samples', []), indent=2)}

Bottom Samples:
{json.dumps(summary.get('bottom_samples', []), indent=2)}

Statistical Summary:
{json.dumps(summary.get('stats', {}), indent=2)}

Task:
- Highlight major trends
- Identify outliers or anomalies
- Suggest 3 actionable recommendations
- Provide an executive summary in 3 bullet points

Return response strictly in this JSON format:
{{
  "key_observations": [...],
  "trends_or_patterns": "...",
  "anomalies_or_outliers": "...",
  "recommendations": [...],
  "summary": [...]
}}
            """

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=1024,
                )
            )
            return self._parse_gemini_response(response)

        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return {"error": str(e), "raw_response": "Failed to generate insight."}

    def _parse_gemini_response(self, response):
        try:
            if hasattr(response, 'text'):
                content = response.text
            elif hasattr(response, 'candidates'):
                content = response.candidates[0].content.parts[0].text
            else:
                content = str(response)

            json_pattern = r'\{[\s\S]*?\}'
            match = re.search(json_pattern, content)

            if match:
                json_str = match.group(0)
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError:
                    cleaned = json_str.replace("'", '"').replace("\n", " ").strip()
                    return json.loads(cleaned)

            return {
                "key_observations": [],
                "trends_or_patterns": "",
                "anomalies_or_outliers": "",
                "recommendations": [],
                "summary": ["Could not parse structured JSON."]
            }

        except Exception as e:
            return {
                "error": str(e),
                "summary": ["Parser failed with error."],
                "raw_response": str(response)
            }

    def generate_vegalite_spec(self, chart_type, x_column, y_column=None, color_column=None, insights=None):
        spec = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
            "description": f"{chart_type.capitalize()} chart of {x_column}" + (f" vs {y_column}" if y_column else ""),
            "data": {"values": self.data.to_dict(orient="records")},
            "width": 600,
            "height": 400,
            "mark": chart_type,
            "encoding": {
                "x": {"field": x_column, "type": "quantitative" if self.data[x_column].dtype in ["int64", "float64"] else "nominal"}
            }
        }

        if y_column:
            spec["encoding"]["y"] = {"field": y_column, "type": "quantitative"}

        if color_column:
            spec["encoding"]["color"] = {"field": color_column, "type": "nominal"}

        if insights and isinstance(insights, dict) and "key_observations" in insights:
            insight_texts = [
                {
                    "data": {"values": [{}]},
                    "mark": {
                        "type": "text",
                        "align": "left",
                        "baseline": "top",
                        "dx": 10,
                        "dy": 10 + 20 * i,
                        "fontSize": 12
                    },
                    "encoding": {
                        "text": {"value": f"• {obs[:100]}"}
                    }
                } for i, obs in enumerate(insights["key_observations"][:3])
            ]
            return {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "description": spec["description"],
                "layer": [spec] + insight_texts
            }

        return spec
