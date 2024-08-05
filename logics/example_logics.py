# logics/example_logics.py

from openai import OpenAI
from prompts.example_prompts import greeting_prompt, summary_prompt
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

def get_greeting():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=greeting_prompt
    )
    return response.choices[0].message.content

def summarize_text(text):
    prompt = summary_prompt.copy()
    prompt[-1]['content'] = prompt[-1]['content'].format(text=text)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt
    )
    return response.choices[0].message.content
