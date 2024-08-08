from openai import OpenAI
import os
from dotenv import load_dotenv


def messages_to_string(messages):
  str = ""
  for item in messages:
    role = item.get('role', '')
    content = item.get('content', '')
    str += f"{role}: {content}\n"
  return str
# dictionary list 형식인 messages를, 하나의 문자열 형식으로 변환합니다.


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

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