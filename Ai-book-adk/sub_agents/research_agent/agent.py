from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from . import tools


research_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="research agent for researching topics, gathering information, and providing insights",
    instruction="""
    You are a research agent specialized in gathering information, analyzing topics, and providing insights.

    """,
    tools=[
        
    ],
)
