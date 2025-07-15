from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.agent_tool import AgentTool
from . import tools
#from ...agent import root_agent               

# Create the thinker agent
thinker_agent = Agent(
    name="thinker_agent",
    model="gemini-2.0-flash",
    description="Thinking agent for planning out the outline of a book, name of chapters, and content of chapters",
    instruction="""
    You are a strategic book planning agent responsible for creating comprehensive book outlines and managing book metadata.
    Your expertise includes:
    - Creating detailed book plans with compelling chapter structures
    - Generating table of contents
    - Designing book cover concepts
    - Managing book metadata and tracking progress
    
    Always ensure your plans are well-structured, engaging, and appropriate for the target audience.
    """,
    #sub_agents=[root_agent],
    tools=[
        #AgentTool(agent = root_agent),
        tools.book_planner_agent,
        tools.table_of_contents_generator,
        tools.book_cover_description_agent,
        tools.store_book_metadata_to_mongodb,
        tools.load_book_metadata_from_mongodb,
        tools.sync_all_books_to_mongodb,
        tools.get_all_books_from_mongodb,
    ],
)
