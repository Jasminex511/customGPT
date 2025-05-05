import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()
logger = logging.getLogger(__name__)

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

def get_schema():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        schema = "Database Schema:\n"
        for table in tables:
            schema += f"- Table: {table}\n"
            columns = inspector.get_columns(table)
            for col in columns:
                schema += f"  - {col['name']} ({col['type']})\n"
        return schema
    except Exception as e:
        logger.error(f"Error fetching schema: {e}")
        raise

def execute_query(sql_query):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            return result.fetchall()
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise
