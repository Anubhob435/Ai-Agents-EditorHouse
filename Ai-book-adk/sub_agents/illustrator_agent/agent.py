from datetime import datetime

from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from .sub_agents.image_description_writer_agent.agent import image_description_weiter_agent
from . import prompt
from . import illustrator


# Create the sales agent
illustrator_agent = Agent(
    name="illustrator_agent",
    model="gemini-2.0-flash",
    description="Illustrator agent for creating illustrations for chapters of a book",
    instruction= prompt.prompt,
    tools=[illustrator.generate_illustration,
           AgentTool(agent = image_description_weiter_agent)],
)
