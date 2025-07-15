# AI Editor House Project Structure

This document outlines the structure of the Editor House project, an AI-powered system for generating books.

## Overall Architecture

The project is a multi-agent system built using the Google Agent Development Kit (ADK). A root agent, `Ai_Book_Writer_and_Editor`, coordinates a team of specialized sub-agents to handle different aspects of the book creation process.

## Agents

The system is composed of the following agents:

- **`Ai_Book_Writer_and_Editor` (Root Agent):** The main agent that orchestrates the entire book generation process. It interacts with the user and delegates tasks to the appropriate sub-agents.

- **`thinker_agent`:** Responsible for planning the book's outline, including chapter titles and a summary of the content for each chapter.

- **`writer_agent`:** Takes the plan from the `thinker_agent` and writes the full content of each chapter.

- **`editor_agent`:** Reviews and edits the generated chapters for clarity, coherence, and style.

- **`illustrator_agent`:** Creates illustrations for the book.
    - It has a sub-agent, `image_description_writer_agent`, which takes a simple prompt and generates a more detailed description for the illustration.
    - It also has a tool, `generate_illustration`, which uses the generated description to create an image and save it to the book's directory.

- **`publisher_agent`:** Responsible for compiling the final book from the individual chapters and illustrations.

## File Structure

- **`Ai-book-adk/`**: The main source code directory.
  - **`agent.py`**: Defines the root agent.
  - **`sub_agents/`**: Contains the definitions for each of the sub-agents.
- **`books/`**: The output directory for the generated books.
  - Each book has its own subdirectory.
  - Each book's directory contains Markdown files for the chapters and an `illustrations/` subdirectory.
- **`others/`**: Contains older or alternative implementations and a simple web interface.
- **`pyproject.toml`**: Manages the project's dependencies.
- **`README.md`**: The project's documentation (currently outdated).
