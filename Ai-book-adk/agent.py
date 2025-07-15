from google.adk.agents import Agent


from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.tool_context import ToolContext
from .sub_agents.editor_agent.agent import editor_agent
from .sub_agents.house_manager_agent.agent import house_manager_agent
from .sub_agents.illustrator_agent.agent import illustrator_agent
from .sub_agents.publisher_agent.agent import publisher_agent
from .sub_agents.thinker_agent.agent import thinker_agent
from .sub_agents.writer_agent.agent import writer_agent
from . import tools

# Create the root customer service agent
ai_book_adk = Agent(
    name="Ai_Book_Writer_and_Editor",
    model="gemini-2.5-flash",
    description="You are an editor House agent that helps users with book generation, formatting, and compilation.",
    instruction="""
    You are the main orchestrator for an AI-powered book creation system.
    You coordinate a team of specialized sub-agents to help users create complete books from concept to publication.
    
    Your capabilities include:
    - Planning and structuring books with the thinker agent
    - Writing content with the writer agent  
    - Editing and refining content with the editor agent
    - Creating illustrations with the illustrator agent
    - Compiling and publishing final books with the publisher agent
    
    You can handle the complete book creation workflow:
    1. Use book_pipeline() to plan a book structure
    2. Use write_next_chapter() to write chapters sequentially
    3. Coordinate sub-agents for specialized tasks
    
    Always guide users through the book creation process step by step.
    After every chapter of a book generated, before proceeding to the next chapter, call the Thinker agent
    to ensure that book meta data was uploaded to mongoDb database.
    
    If users have questions about Editor House, services, or need general guidance, 
    delegate to the House Manager agent who can provide comprehensive information.
    """,
    sub_agents=[editor_agent, house_manager_agent, illustrator_agent, publisher_agent, thinker_agent, writer_agent],
    tools=[
        tools.book_pipeline,
        tools.write_next_chapter,
        AgentTool(agent = editor_agent),
        AgentTool(agent = house_manager_agent),
        AgentTool(agent = illustrator_agent),
        AgentTool(agent = publisher_agent),
        AgentTool(agent = thinker_agent),
        AgentTool(agent = writer_agent),
    ],
)

root_agent = ai_book_adk