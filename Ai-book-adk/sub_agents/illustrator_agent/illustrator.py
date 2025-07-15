import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import datetime
import logging
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Initialize the client with the API key
client = genai.Client(api_key=api_key)

def generate_illustration(description: str, prefix: str = "illustration", book_path: Optional[str] = None) -> Optional[str]:
    """
    Generate an illustration based on the provided description
    
    Args:
        description: A text description of what to generate
        prefix: A prefix for the filename (default: 'illustration')
        book_path: Path to the book folder where illustrations should be saved
        
    Returns:
        The file path of the saved illustration, or None if generation failed
    """
    # Determine where to save the illustrations
    if book_path:
        # Save in the book's illustrations directory
        illustrations_dir = os.path.join(book_path, 'illustrations')
    else:
        # Fallback to default location
        illustrations_dir = os.path.join(os.path.dirname(__file__), 'illustrations')
    
    # Create illustrations directory if it doesn't exist
    if not os.path.exists(illustrations_dir):
        os.makedirs(illustrations_dir)
    
    # Clean up prefix to ensure it's filename-safe and reasonably short
    safe_prefix = prefix.replace(" ", "_").replace(":", "")[:30].lower()  # Limit to 30 chars
    
    # Call the AI model to generate the image
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=description,
        config=types.GenerateContentConfig(
          response_modalities=['Text', 'Image']
        )
    )

    # Generate a unique filename using timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_prefix}_{timestamp}.png"
    filepath = os.path.join(illustrations_dir, filename)

    # Process and save the generated image
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            logger.info(f"Image generation note: {part.text}")
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(filepath)
            logger.info(f"Image saved to: {filepath}")
            return filepath
    
    # If no image was generated, return None
    logger.warning("No image was generated")
    return None

