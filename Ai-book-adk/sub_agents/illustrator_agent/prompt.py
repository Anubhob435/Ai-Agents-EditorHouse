prompt ="""    Generate an illustration based on the provided description, if sufficient description
is not found use the image description writer agent to generate a description.
    
    Args:
        description: A text description of what to generate
        prefix: A prefix for the filename (default: 'illustration')
        book_path: Path to the book folder where illustrations should be saved
        
    Returns:
        The file path of the saved illustration"""