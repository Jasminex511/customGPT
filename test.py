import openai
import os
from flask.cli import load_dotenv

# Make sure the API key is set
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Making the API request using the correct endpoint for chat models
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # You can use "gpt-4" as well if you have access
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"}
    ],
    max_tokens=5  # Small token output for testing
)

print(response)
