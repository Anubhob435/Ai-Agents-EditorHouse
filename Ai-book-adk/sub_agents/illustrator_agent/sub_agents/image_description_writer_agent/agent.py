from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.tool_context import ToolContext

# Create the sales agent
image_description_weiter_agent = Agent(
    name="image_description_weiter_agent",
    model="gemini-2.0-flash",
    description="Agent that can werite image descriptions for illustrations",
    instruction="""
    You are an agent that can write image descriptions for illustrations from a single line or word.
    If needed you can search the web for more information.
    """,
    tools=[google_search],
)
