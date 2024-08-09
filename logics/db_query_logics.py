import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import prompts.query_db_prompts as query_db_prompts
import streamlit as st

# load_dotenv()
# openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_key = st.secrets['openai_api_key']

client = OpenAI(api_key=openai_api_key)


def make_query_for_db(clear_query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = query_db_prompts.query_for_db
    ).choices[0].message.content

    return response