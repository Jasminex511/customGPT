import streamlit as st
import snowflake.connector
import os
import openai
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Snowflake connection
def connect_to_db():
    try:
        logging.info("Attempting to connect to Snowflake...")
        conn = snowflake.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            account=os.getenv("DB_HOST"),
            warehouse="COMPUTE_WH",
            database=os.getenv("DB_NAME"),
            schema="COMPANY"
        )
        logging.info("Successfully connected to Snowflake.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to Snowflake: {e}")
        st.error(f"Failed to connect to Snowflake: {e}")
        raise

# Fetch database schema
def get_schema():
    try:
        logging.info("Fetching database schema...")
        conn = connect_to_db()
        cursor = conn.cursor()

        # Fetch table names
        logging.info("Fetching table names...")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        logging.info(f"Found {len(tables)} tables.")

        schema = "Database Schema:\n"
        for table in tables:
            table_name = table[1]  # Table name is in the second column
            schema += f"- Table: {table_name}\n"

            # Fetch column details
            logging.info(f"Fetching columns for table: {table_name}...")
            cursor.execute(f"DESCRIBE TABLE {table_name};")
            columns = cursor.fetchall()
            logging.info(f"Found {len(columns)} columns in table {table_name}.")
            for column in columns:
                column_name = column[0]  # Column name is in the first column
                data_type = column[1]  # Data type is in the second column
                schema += f"  - {column_name} ({data_type})\n"

        cursor.close()
        conn.close()
        logging.info("Successfully fetched database schema.")
        return schema
    except Exception as e:
        logging.error(f"Failed to fetch database schema: {e}")
        st.error(f"Failed to fetch database schema: {e}")
        raise

# Generate SQL using GPT
# Generate SQL using GPT
def generate_sql(natural_language_query):
    try:
        schema = get_schema()  # Dynamically fetch schema
        prompt = f"""
                You are a SQL expert. Given the following database schema:
                {schema}

                Translate the following natural language query into a valid SQL query without any extra formatting or code blocks:
                "{natural_language_query}"
                """
        logging.info("Generating SQL query using GPT.")

        # Use the chat-based API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a SQL expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # Adjust token limit if necessary
        )
        sql_query = response['choices'][0]['message']['content'].strip()
        logging.info(f"Generated SQL: {sql_query}")
        return sql_query
    except Exception as e:
        logging.error(f"Failed to generate SQL: {e}")
        raise

# Execute SQL query
def execute_query(sql_query):
    try:
        logging.info(f"Executing SQL query: {sql_query}")
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info("Successfully executed SQL query.")
        return results
    except Exception as e:
        logging.error(f"Failed to execute SQL query: {e}")
        st.error(f"Failed to execute SQL query: {e}")
        raise

# Streamlit app
def main():
    st.title("Natural Language to SQL Query")
    st.write("Enter a natural language query, and we'll generate and execute the corresponding SQL query.")

    # Input: Natural language query
    natural_language_query = st.text_input("Enter your query (e.g., 'Show me the total sales for January 2024'):")

    if st.button("Generate SQL and Execute"):
        if natural_language_query:
            try:
                # Step 1: Generate SQL
                sql_query = generate_sql(natural_language_query)
                st.write(f"Generated SQL: `{sql_query}`")

                # Step 2: Execute SQL
                results = execute_query(sql_query)

                # Step 3: Display results
                st.write("Query Results:")
                st.table(results)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query.")

if __name__ == '__main__':
    main()