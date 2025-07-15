"""    Generates illustration based on the provided description
    
    Args:
        description: A text description of what to generate
        prefix: A prefix for the filename (default: 'illustration')
        book_path: Path to the book folder where illustrations should be saved
        
    Returns:
        The file path of the saved illustration
"""

from .agent import illustrator_agent
__all__ = ["illustrator_agent"]

from .illustrator import generate_illustration