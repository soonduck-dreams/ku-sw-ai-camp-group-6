from openai import OpenAI
import os
from dotenv import load_dotenv
import time
import streamlit as st


def messages_to_string(messages):
  max_length_to_display = 10000
  str = ""
  for item in messages:
    role = item.get('role', '')
    content = item.get('content', '')
    str += f"\n\033[1m\033[32m{role}\033[0m: {content[:max_length_to_display] + '...' if len(content) > max_length_to_display else content}\n"

  return str
# dictionary list 형식인 messages를, 하나의 문자열 형식으로 변환합니다.


load_dotenv()
# openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_key = st.secrets['OPENAI_API_KEY']

client = OpenAI(api_key=openai_api_key)

def get_embedding(input):
    """input을 임베딩한 결과를 return하는 함수
    Args:
        input (string): 임베딩할 string
    """
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data


def print_messages_to_string(messages, interval=0.5):
  max_length_to_display = 10000
  for item in messages:
    role = item.get('role', '')
    content = item.get('content', '')
    print(f"\n\033[1m\033[32m{role}\033[0m: {content[:max_length_to_display] + '...' if len(content) > max_length_to_display else content}\n")
    time.sleep(interval)
# 시연을 위해 내부 프롬프트들을 터미널에 표시해줍니다.