Looking at your main.py file and the sub-agent structure, here's how I would divide the functionality across the different agents:

## **1. Thinker Agent** 
*Planning and conceptual work*

````python
# Functions to move to thinker_agent:
- book_planner_agent()
- table_of_contents_generator() 
- book_cover_description_agent()
- BookMetadata class (metadata management)
````

**Responsibilities:**
- Book planning and structure
- Metadata management and tracking
- Table of contents generation
- Cover concept development
- Book status tracking and reporting

## **2. Writer Agent**
*Content creation*

````python
# Functions to move to writer_agent:
- headline_agent()
- writer_agent() 
- chapter_writer_agent()
- story_pipeline()
````

**Responsibilities:**
- Story/chapter writing
- Title generation
- Creative content generation
- Single story creation pipeline

## **3. Editor Agent**
*Content refinement and formatting*

````python
# Functions to move to editor_agent:
- editor_agent()
- chapter_editor_agent()
- FormatAgent class (already exists)
````

**Responsibilities:**
- Grammar and style editing
- Content refinement
- Advanced formatting
- Quality assurance

## **4. Illustrator Agent**
*Visual content creation*

````python
# Functions to move to illustrator_agent:
- illustrator_agent()
- generate_illustration() (already exists)
````

**Responsibilities:**
- Chapter illustration generation
- Visual content creation
- Image processing and saving

## **5. Publisher Agent**
*Final compilation and output*

````python
# Functions to move to publisher_agent:
- publisher_agent()
- compile_book()
- get_book_status()
````

**Responsibilities:**
- File management and saving
- Book compilation
- Final output generation
- Status reporting and book management

## **Main Agent (Root)**
*Orchestration and workflow*

````python
# Functions to keep in main agent:
- book_pipeline()
- write_next_chapter()
- Workflow orchestration
- Agent coordination
````

**Responsibilities:**
- Orchestrate the entire book creation process
- Coordinate between sub-agents
- Manage the overall workflow
- Handle user interactions

This division follows the **separation of concerns** principle where each agent has a specific role in the book creation pipeline, making the system more modular and maintainable.