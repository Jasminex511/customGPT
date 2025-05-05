import openai
import os
from dotenv import load_dotenv
from db_utils import get_schema

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_sql(nl_query):
    schema = get_schema()
    prompt = f"""
    You are a SQL expert. Given the schema below, generate a SQL query for:
    "{nl_query}"

    Schema:
    {schema}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()
