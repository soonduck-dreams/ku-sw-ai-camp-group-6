# logics/utils.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import faiss
import numpy as np

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

def messages_to_string(messages):
  str = ""
  for item in messages:
    role = item.get('role', '')
    content = item.get('content', '')
    str += f"{role}: {content}\n"
  return str
# dictionary list 형식인 messages를, 하나의 문자열 형식으로 변환합니다.

def get_embedding(input):
    """input(text)를 받아 embedding된 값 (float list)을 return
    """
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data