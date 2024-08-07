# logics/main_logics.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy
import logics.utils as utils
import logics.query_logics as query_logics

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)





def answer_art(messages, db_art, db_etc):
    #사용자의 질문에 대해 답하는 기본 함수 만드는 중
    #messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
    #ask: 사용자의 질문
    #db_art: 예술품 DB, db_etc: 기타 DB
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]} for m in messages
        ]
        + [
            {"user": "user", "content": ask},
            #{"role": "system", "content": system_message}
        ],
        stream=True
    )
    return stream