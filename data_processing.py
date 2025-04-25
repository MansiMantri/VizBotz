# import pandas as pd
# import requests
# import json
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# class Process_data:

#     def __init__(self, data):
#         self.data = pd.read_csv(data)
#         # Load environment variables for API keys
#         load_dotenv()
#         # Add Gemini API key only
#         self.gemini_api_key = os.getenv("GEMINI_API_KEY")
#         # Configure Gemini
#         if self.gemini_api_key:
#             genai.configure(api_key=self.gemini_api_key)

#     def get_df(self):
#         return self.data

#     def get_columns(self):
#         return self.data.columns.to_list()

#     def get_bar_data(self):
#         return self.data

#     def get_mean(self, col_name):
#         return self.data[col_name].mean()

#     def describe_data(self):
#         return self.data.describe()
        
#     def generate_insights(self, chart_type, x_column, y_column=None, color_column=None):
#         """
#         Generate insights about the data visualization using Google Gemini API
        
#         Args:
#             chart_type (str): Type of chart (bar, scatter, line, etc.)
#             x_column (str): Column used for x-axis
#             y_column (str): Column used for y-axis (if applicable)
#             color_column (str): Column used for color differentiation (if applicable)
            
#         Returns:
#             dict: JSON response containing insights
#         """
#         # Prepare data for API request
#         data_sample = self.data.head(50).to_dict(orient='records')  # Limit sample size
        
#         # Create a description of the visualization
#         viz_description = f"A {chart_type} chart showing {x_column}"
#         if y_column:
#             viz_description += f" vs {y_column}"
#         if color_column:
#             viz_description += f" with color differentiation by {color_column}"
            
#         # Prepare statistics to help the model
#         stats = {}
#         if x_column:
#             stats[f"{x_column}_stats"] = self.data[x_column].describe().to_dict()
#         if y_column:
#             stats[f"{y_column}_stats"] = self.data[y_column].describe().to_dict()
            
#         # Create prompt for Gemini API
#         prompt = f"""
#         Analyze this {chart_type} chart visualization and provide insights:

#         Chart Description: {viz_description}

#         Data Sample: {json.dumps(data_sample[:5])}  # First 5 records for brevity

#         Statistics: {json.dumps(stats)}

#         Please provide the following in JSON format:
#         {{
#             "key_observations": ["observation 1", "observation 2", "observation 3"],
#             "trends_or_patterns": "description of trends",
#             "anomalies_or_outliers": "description of anomalies",
#             "recommendations": "recommendations for further analysis",
#             "summary": "concise summary"
#         }}
#         """

#         # Call Gemini API
#         try:
#             response = self._call_gemini_api(prompt)
#             insights = self._parse_gemini_response(response)
#             return insights
#         except Exception as e:
#             print(f"Error generating insights: {str(e)}")
#             return {"error": str(e), "message": "Failed to generate insights"}

#     def _call_gemini_api(self, prompt):
#         """
#         Call the Google Gemini API.
#         """
#         if not self.gemini_api_key:
#             raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your environment variables.")
        
#         try:
#             # List available models to debug
#             models = genai.list_models()
#             print("Available models:")
#             for model in models:
#                 print(f"- {model.name}")
                
#             # Try to use gemini-1.5-flash first (recommended replacement)
#             try:
#                 model = genai.GenerativeModel("gemini-1.5-flash")
#                 response = model.generate_content(
#                     prompt,
#                     generation_config=genai.types.GenerationConfig(
#                         temperature=0.3,
#                         max_output_tokens=1024,
#                     )
#                 )
#                 return response
#             except Exception as e1:
#                 print(f"Failed with gemini-1.5-flash: {str(e1)}")
                
#                 # Try gemini-1.5-pro as fallback
#                 try:
#                     model = genai.GenerativeModel("gemini-1.5-pro")
#                     response = model.generate_content(prompt)
#                     return response
#                 except Exception as e2:
#                     print(f"Failed with gemini-1.5-pro: {str(e2)}")
                    
#                     # Try gemini-pro as final fallback (if still available)
#                     model = genai.GenerativeModel("gemini-pro")
#                     response = model.generate_content(prompt)
#                     return response
                    
#         except Exception as e:
#             print(f"All Gemini API attempts failed: {str(e)}")
            
#             # Create a simple fallback response with statistical insights
#             return self._generate_statistical_insights_fallback(prompt)
            
#     def _generate_statistical_insights_fallback(self, prompt):
#         """
#         Generate basic statistical insights as a fallback when API calls fail.
#         Creates a response object with a text attribute to mimic Gemini's response format.
#         """
#         # Extract chart type and columns from the prompt
#         import re
#         chart_match = re.search(r'A (\w+) chart showing (\w+)(?:\s+vs\s+(\w+))?', prompt)
        
#         if not chart_match:
#             # Create a simple response object
#             class FallbackResponse:
#                 def __init__(self, text):
#                     self.text = text
                    
#             error_text = '{"key_observations": ["Unable to generate insights due to API error"], "summary": "API error occurred", "trends_or_patterns": "No data available", "anomalies_or_outliers": "No data available", "recommendations": "Try again later"}'
#             return FallbackResponse(error_text)
        
#         chart_type = chart_match.group(1)
#         x_column = chart_match.group(2)
#         y_column = chart_match.group(3) if chart_match.group(3) else None
        
#         # Generate basic statistical insights
#         insights = {
#             "key_observations": [],
#             "trends_or_patterns": "",
#             "anomalies_or_outliers": "",
#             "recommendations": "",
#             "summary": f"Basic statistical analysis of {chart_type} chart"
#         }
        
#         # Add basic statistics for x_column
#         if x_column in self.data.columns:
#             x_stats = self.data[x_column].describe()
#             insights["key_observations"].append(f"The {x_column} has {len(self.data[x_column])} data points")
            
#             if self.data[x_column].dtype in ['int64', 'float64']:
#                 insights["key_observations"].append(f"The {x_column} values range from {x_stats['min']:.2f} to {x_stats['max']:.2f}")
#                 insights["key_observations"].append(f"The average {x_column} is {x_stats['mean']:.2f}")
        
#         # Add basic statistics for y_column if it exists
#         if y_column and y_column in self.data.columns:
#             y_stats = self.data[y_column].describe()
            
#             if self.data[y_column].dtype in ['int64', 'float64']:
#                 insights["key_observations"].append(f"The average {y_column} is {y_stats['mean']:.2f}")
                
#                 # Check for correlation if both columns are numeric
#                 if self.data[x_column].dtype in ['int64', 'float64']:
#                     corr = self.data[x_column].corr(self.data[y_column])
#                     if abs(corr) > 0.7:
#                         insights["trends_or_patterns"] = f"Strong {'positive' if corr > 0 else 'negative'} correlation ({corr:.2f}) between {x_column} and {y_column}"
#                     elif abs(corr) > 0.3:
#                         insights["trends_or_patterns"] = f"Moderate {'positive' if corr > 0 else 'negative'} correlation ({corr:.2f}) between {x_column} and {y_column}"
#                     else:
#                         insights["trends_or_patterns"] = f"Weak correlation ({corr:.2f}) between {x_column} and {y_column}"
        
#         # Create a simple response object with the insights as JSON
#         class FallbackResponse:
#             def __init__(self, text):
#                 self.text = text
                
#         return FallbackResponse(json.dumps(insights))
        
#     def _parse_gemini_response(self, response):
#         """
#         Parse the Gemini API response to extract insights.
        
#         Args:
#             response: The API response from Gemini.
            
#         Returns:
#             dict: Structured insights data.
#         """
#         try:
#             # Extract the content from the response
#             content = response.text
            
#             # Try to find and parse JSON in the response
#             import re
#             json_pattern = r'\{[\s\S]*\}'
#             json_match = re.search(json_pattern, content)
            
#             if json_match:
#                 json_str = json_match.group(0)
#                 try:
#                     insights = json.loads(json_str)
#                     return insights
#                 except json.JSONDecodeError:
#                     # Try to clean the JSON string
#                     cleaned_json = json_str.replace("'", '"').replace('\n', ' ')
#                     try:
#                         insights = json.loads(cleaned_json)
#                         return insights
#                     except:
#                         pass # Fall through if cleaning fails
            
#             # If no valid JSON found, structure the text response
#             insights = {
#                 "key_observations": [content],
#                 "summary": content[:200] + "..." if len(content) > 200 else content,
#                 "trends_or_patterns": "Could not parse structured JSON from response.",
#                 "anomalies_or_outliers": "",
#                 "recommendations": ""
#             }
            
#             return insights
#         except Exception as e:
#             # Attempt to get raw response content even in case of error during parsing
#             raw_content = "Failed to extract content"
#             try:
#                 raw_content = response.text
#             except:
#                 raw_content = str(response)
                
#             return {
#                 "error": f"Error parsing Gemini response: {str(e)}",
#                 "raw_response": raw_content
#             }
    
#     def generate_vegalite_spec(self, chart_type, x_column, y_column=None, color_column=None, insights=None):
#         """
#         Generate a Vega-Lite specification for the visualization with insights
        
#         Args:
#             chart_type (str): Type of chart (bar, scatter, line, etc.)
#             x_column (str): Column used for x-axis
#             y_column (str): Column used for y-axis (if applicable)
#             color_column (str): Column used for color differentiation (if applicable)
#             insights (dict): Insights data to include in the visualization
            
#         Returns:
#             dict: Vega-Lite specification
#         """
#         # Base specification
#         spec = {
#             "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
#             "description": f"{chart_type.capitalize()} chart of {x_column}" + (f" vs {y_column}" if y_column else ""),
#             "data": {"values": self.data.to_dict(orient='records')},
#             "width": 600,
#             "height": 400
#         }
        
#         # Configure the mark based on chart type
#         if chart_type == "bar":
#             spec["mark"] = "bar"
#         elif chart_type == "line":
#             spec["mark"] = "line"
#         elif chart_type == "scatter":
#             spec["mark"] = "point"
#         elif chart_type == "area":
#             spec["mark"] = "area"
#         else:
#             spec["mark"] = "bar"  # Default
            
#         # Configure encoding
#         encoding = {
#             "x": {"field": x_column, "type": "nominal" if self.data[x_column].dtype == 'object' else "quantitative"}
#         }
        
#         if y_column:
#             encoding["y"] = {"field": y_column, "type": "quantitative"}
        
#         if color_column:
#             encoding["color"] = {"field": color_column, "type": "nominal"}
            
#         spec["encoding"] = encoding
        
#         # Add insights if provided
#         if insights and not isinstance(insights, str) and not insights.get('error'):
#             # Create a text layer for insights
#             insights_layer = {
#                 "data": {"values": [{}]},  # Empty data as we just want to display text
#                 "mark": {
#                     "type": "text",
#                     "align": "left",
#                     "baseline": "top",
#                     "dx": 5,
#                     "dy": 5,
#                     "fontSize": 12
#                 },
#                 "encoding": {
#                     "text": {"value": "Key Insights:"}
#                 }
#             }
            
#             # Create bullet points for key observations
#             if "key_observations" in insights and insights["key_observations"]:
#                 bullet_points = []
#                 for i, observation in enumerate(insights["key_observations"]):
#                     if i < 3:  # Limit to 3 observations
#                         bullet_points.append({
#                             "data": {"values": [{}]},
#                             "mark": {
#                                 "type": "text",
#                                 "align": "left",
#                                 "baseline": "top",
#                                 "dx": 10,
#                                 "dy": 25 + (i * 20),
#                                 "fontSize": 11
#                             },
#                             "encoding": {
#                                 "text": {"value": f"• {observation[:100]}..." if len(observation) > 100 else f"• {observation}"}
#                             }
#                         })
                
#                 # Convert to a layered chart with insights
#                 spec = {
#                     "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
#                     "description": spec["description"],
#                     "layer": [spec, insights_layer] + bullet_points
#                 }
            
#         return spec
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
