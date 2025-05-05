import streamlit as st
import logging
from db_utils import execute_query
from gpt_utils import generate_sql

logging.basicConfig(level=logging.INFO)

st.title("Natural Language to SQL")

query = st.text_input("Enter a natural language query:")

if st.button("Generate SQL and Execute"):
    if query:
        try:
            sql = generate_sql(query)
            st.code(sql, language="sql")
            results = execute_query(sql)
            st.table(results)
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter a query.")
