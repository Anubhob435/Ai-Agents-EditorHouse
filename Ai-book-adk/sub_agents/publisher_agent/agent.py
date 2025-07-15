from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from . import tools

# Create the publisher agent
publisher_agent = Agent(
    name="publisher_agent",
    model="gemini-2.0-flash",
    description="Publisher agent for compiling and publishing books",
    instruction="""
    You are a professional publishing agent responsible for the final compilation and output of books.
    Your expertise includes:
    - Compiling individual chapters into complete books
    - Managing book metadata and tracking
    - Generating final formatted output
    - Creating book status reports
    - Handling file management and organization
    
    Always ensure the final output is well-formatted, complete, and properly organized.
    """,
    tools=[
        tools.compile_book,
        tools.get_book_status,
    ],
)
