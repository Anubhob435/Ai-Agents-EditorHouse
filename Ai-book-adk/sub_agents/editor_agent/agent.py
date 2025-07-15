from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from . import tools

# Create the editor agent
editor_agent = Agent(
    name="editor_agent",
    model="gemini-2.0-flash",
    description="Editor agent for editing chapters of a book and improving content quality",
    instruction="""
    You are a professional editor specialized in improving written content quality.
    Your expertise includes:
    - Grammar and style editing
    - Improving clarity and flow
    - Maintaining the author's voice and creative style
    - Ensuring narrative coherence and consistency
    
    Always preserve the original creative intent while enhancing readability and quality.
    Focus on improving grammar, clarity, and flow without changing the core content or style.
    """,
    tools=[
        tools.editor_agent,
        tools.publish_story,
        tools.chapter_editor_agent,
    ],
)
