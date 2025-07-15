"""Tools for the House Manager Agent."""

import json
from datetime import datetime
from typing import Dict, List, Any

def get_house_services() -> str:
    """
    Provides comprehensive information about all services offered by Editor House.
    
    Returns:
        str: Detailed information about Editor House services
    """
    services = {
        "book_creation": {
            "description": "Complete book writing and editing services",
            "features": [
                "AI-powered content generation",
                "Professional editing and proofreading",
                "Chapter-by-chapter development",
                "Plot and structure planning",
                "Character development assistance"
            ],
            "agents_involved": ["Writer Agent", "Editor Agent", "Thinker Agent"]
        },
        "illustration_services": {
            "description": "Visual content creation for books",
            "features": [
                "Cover design and illustration",
                "Character illustrations",
                "Scene illustrations",
                "Infographics and diagrams",
                "Image description generation"
            ],
            "agents_involved": ["Illustrator Agent", "Image Description Writer Agent"]
        },
        "publishing_services": {
            "description": "Book compilation and publishing assistance",
            "features": [
                "Format conversion (PDF, EPUB, etc.)",
                "Layout and formatting",
                "Publishing platform integration",
                "Distribution guidance",
                "Metadata management"
            ],
            "agents_involved": ["Publisher Agent"]
        },
        "planning_services": {
            "description": "Strategic book planning and organization",
            "features": [
                "Book outline creation",
                "Table of contents generation",
                "Chapter planning",
                "Progress tracking",
                "Database management"
            ],
            "agents_involved": ["Thinker Agent"]
        }
    }
    
    return json.dumps(services, indent=2)

def get_house_agents_info() -> str:
    """
    Provides detailed information about all agents working in Editor House.
    
    Returns:
        str: Information about each agent and their capabilities
    """
    agents_info = {
        "main_orchestrator": {
            "name": "AI Book Writer and Editor",
            "role": "Main coordinator for book creation workflow",
            "capabilities": [
                "Orchestrates entire book creation process",
                "Coordinates between specialized agents",
                "Manages book pipeline",
                "Handles user interactions"
            ]
        },
        "writer_agent": {
            "name": "Writer Agent",
            "role": "Content creation specialist",
            "capabilities": [
                "Writes book chapters",
                "Creates engaging narratives",
                "Develops characters and plots",
                "Adapts writing style to requirements"
            ]
        },
        "editor_agent": {
            "name": "Editor Agent",
            "role": "Content refinement specialist",
            "capabilities": [
                "Proofreads and edits content",
                "Improves readability and flow",
                "Ensures consistency",
                "Suggests improvements"
            ]
        },
        "illustrator_agent": {
            "name": "Illustrator Agent",
            "role": "Visual content creator",
            "capabilities": [
                "Creates book illustrations",
                "Designs book covers",
                "Generates visual descriptions",
                "Manages image workflows"
            ]
        },
        "publisher_agent": {
            "name": "Publisher Agent",
            "role": "Book compilation and publishing specialist",
            "capabilities": [
                "Formats books for publication",
                "Converts between formats",
                "Manages publishing workflows",
                "Handles distribution preparation"
            ]
        },
        "thinker_agent": {
            "name": "Thinker Agent",
            "role": "Strategic planning and organization specialist",
            "capabilities": [
                "Creates book outlines",
                "Plans chapter structures",
                "Manages book metadata",
                "Tracks progress in database"
            ]
        },
        "house_manager": {
            "name": "House Manager",
            "role": "Information and guidance specialist",
            "capabilities": [
                "Provides information about Editor House",
                "Explains services and capabilities",
                "Guides users through processes",
                "Answers questions about the house"
            ]
        }
    }
    
    return json.dumps(agents_info, indent=2)
    """
    Provides detailed information about all agents working in Editor House.
    
    Returns:
        str: Information about each agent and their capabilities
    """
    agents_info = {
        "main_orchestrator": {
            "name": "AI Book Writer and Editor",
            "role": "Main coordinator for book creation workflow",
            "capabilities": [
                "Orchestrates entire book creation process",
                "Coordinates between specialized agents",
                "Manages book pipeline",
                "Handles user interactions"
            ]
        },
        "writer_agent": {
            "name": "Writer Agent",
            "role": "Content creation specialist",
            "capabilities": [
                "Writes book chapters",
                "Creates engaging narratives",
                "Develops characters and plots",
                "Adapts writing style to requirements"
            ]
        },
        "editor_agent": {
            "name": "Editor Agent",
            "role": "Content refinement specialist",
            "capabilities": [
                "Proofreads and edits content",
                "Improves readability and flow",
                "Ensures consistency",
                "Suggests improvements"
            ]
        },
        "illustrator_agent": {
            "name": "Illustrator Agent",
            "role": "Visual content creator",
            "capabilities": [
                "Creates book illustrations",
                "Designs book covers",
                "Generates visual descriptions",
                "Manages image workflows"
            ]
        },
        "publisher_agent": {
            "name": "Publisher Agent",
            "role": "Book compilation and publishing specialist",
            "capabilities": [
                "Formats books for publication",
                "Converts between formats",
                "Manages publishing workflows",
                "Handles distribution preparation"
            ]
        },
        "thinker_agent": {
            "name": "Thinker Agent",
            "role": "Strategic planning and organization specialist",
            "capabilities": [
                "Creates book outlines",
                "Plans chapter structures",
                "Manages book metadata",
                "Tracks progress in database"
            ]
        },
        "house_manager": {
            "name": "House Manager",
            "role": "Information and guidance specialist",
            "capabilities": [
                "Provides information about Editor House",
                "Explains services and capabilities",
                "Guides users through processes",
                "Answers questions about the house"
            ]
        }
    }
    
    return json.dumps(agents_info, indent=2)

def get_book_creation_workflow() -> str:
    """
    Provides step-by-step information about the book creation workflow.
    
    Returns:
        str: Detailed workflow information
    """
    workflow = {
        "book_creation_process": {
            "step_1": {
                "title": "Initial Planning",
                "description": "Book concept and outline creation",
                "agent": "Thinker Agent",
                "tasks": [
                    "Create book outline",
                    "Plan chapter structure",
                    "Generate table of contents",
                    "Set up book metadata"
                ]
            },
            "step_2": {
                "title": "Content Creation",
                "description": "Writing book chapters",
                "agent": "Writer Agent",
                "tasks": [
                    "Write chapter content",
                    "Develop characters and plot",
                    "Create engaging narratives",
                    "Follow outline structure"
                ]
            },
            "step_3": {
                "title": "Content Refinement",
                "description": "Editing and proofreading",
                "agent": "Editor Agent",
                "tasks": [
                    "Review and edit content",
                    "Improve readability",
                    "Ensure consistency",
                    "Polish language and style"
                ]
            },
            "step_4": {
                "title": "Visual Enhancement",
                "description": "Adding illustrations and visuals",
                "agent": "Illustrator Agent",
                "tasks": [
                    "Create book cover",
                    "Generate illustrations",
                    "Design visual elements",
                    "Enhance visual appeal"
                ]
            },
            "step_5": {
                "title": "Final Compilation",
                "description": "Publishing and formatting",
                "agent": "Publisher Agent",
                "tasks": [
                    "Format for publication",
                    "Convert to required formats",
                    "Prepare for distribution",
                    "Finalize publication"
                ]
            }
        }
    }
    
    return json.dumps(workflow, indent=2)

def answer_house_faq(question: str = "") -> str:
    """
    Answers frequently asked questions about Editor House services.
    
    Args:
        question: The question to answer
        
    Returns:
        str: Answer to the question or list of FAQs
    """
    faqs = {
        "what is editor house": "Editor House is an AI-powered book creation platform that uses specialized agents to help you write, edit, illustrate, and publish complete books from concept to publication.",
        
        "how does the book creation process work": "The process involves 5 main steps: 1) Planning with Thinker Agent, 2) Writing with Writer Agent, 3) Editing with Editor Agent, 4) Illustration with Illustrator Agent, and 5) Publishing with Publisher Agent.",
        
        "what types of books can you create": "We can create various types of books including fiction novels, non-fiction books, children's books, educational materials, technical documentation, and more.",
        
        "how long does it take to create a book": "The time depends on the book's complexity and length. Simple books can be created in hours, while complex novels may take several days.",
        
        "can i customize the writing style": "Yes, our Writer Agent can adapt to various writing styles, genres, and tones based on your specifications.",
        
        "do you provide illustrations": "Yes, our Illustrator Agent can create custom illustrations, book covers, and visual elements for your book.",
        
        "what formats can you publish in": "Our Publisher Agent can format books for various formats including PDF, EPUB, MOBI, and print-ready formats.",
        
        "can i track the progress": "Yes, the Thinker Agent maintains metadata and progress tracking in our database system.",
        
        "how do i get started": "Simply describe your book idea to our main AI Book Writer and Editor agent, and it will guide you through the entire process.",
        
        "is the content original": "Yes, all content is generated using AI and is original. However, we recommend reviewing for any potential similarities to existing works."
    }
    
    if question:
        question_lower = question.lower()
        for faq_key, answer in faqs.items():
            if any(word in question_lower for word in faq_key.split()):
                return f"Q: {question}\nA: {answer}"
        return f"I don't have a specific answer for '{question}', but I can help you with information about Editor House services. Would you like to know about our book creation process, agents, or services?"
    else:
        faq_list = "\n\n".join([f"Q: {q.title()}\nA: {a}" for q, a in faqs.items()])
        return f"Frequently Asked Questions about Editor House:\n\n{faq_list}"

def get_house_status() -> str:
    """
    Provides current operational status and statistics of Editor House.
    
    Returns:
        str: Current status information
    """
    status = {
        "operational_status": "Fully Operational",
        "timestamp": datetime.now().isoformat(),
        "available_agents": [
            "AI Book Writer and Editor (Main Orchestrator)",
            "Writer Agent",
            "Editor Agent",
            "Illustrator Agent",
            "Publisher Agent",
            "Thinker Agent",
            "House Manager"
        ],
        "active_services": [
            "Book Creation Pipeline",
            "Content Writing",
            "Professional Editing",
            "Illustration Services",
            "Publishing Services",
            "Strategic Planning",
            "Information Services"
        ],
        "supported_formats": [
            "PDF",
            "EPUB",
            "MOBI",
            "Print-ready formats",
            "Web formats"
        ],
        "capabilities": {
            "concurrent_projects": "Multiple",
            "languages_supported": "Multiple (AI-driven)",
            "genres_supported": "All genres",
            "collaboration": "Multi-agent coordination"
        }
    }
    
    return json.dumps(status, indent=2)
