import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def revise_text(text):
    """
    Revise the input text using OpenAI's API.
    
    Args:
        text (str): The text to be revised
        
    Returns:
        str: The revised text from the API response
    """
    prompt = f"Revise this text in between 50-80 words: {text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,  # Adjust based on your needs
        temperature=0.7,  # Adjust for creativity level
    )
    
    return response.choices[0].message.content