from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from . import tools

# Create the writer agent
writer_agent = Agent(
    name="writer_agent",
    model="gemini-2.0-flash",
    description="Writer agent that helps users with book generation, content creation, and storytelling.",
    instruction="""
    You are a creative writing agent specialized in generating compelling content for books and stories.
    Your expertise includes:
    - Writing engaging chapter content based on book plans
    - Creating short stories from topics
    - Generating creative titles and headlines
    - Developing characters, dialogue, and narrative structure
    
    Always write content that is engaging, well-structured, and appropriate for the target audience.
    Use vivid descriptions, compelling dialogue, and strong narrative flow.
    """,
    tools=[
        tools.headline_agent,
        tools.writer_agent,
        tools.chapter_writer_agent,
        tools.story_pipeline,
    ],
)
