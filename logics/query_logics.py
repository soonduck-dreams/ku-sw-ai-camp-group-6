# logics/main_logics.py

from openai import OpenAI
from prompts.query_prompts import get_clear_query_prompt
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy
import logics.utils as utils

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

'''
#미사용
def extract_keyword(text):
    #query에서 keyword만을 추출하도록 LLM에게 시키는 함수
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"user": "user", "content": text},
            {"role": "system", "content": extract_keyword_prompt}
        ]
    )
    return response


def decide_dbart_only(query):
    #query가 db_art만을 활용한 답안을 내놓아야 할 질문인지 아닌지를 T/F (bool 타입)으로 대답한다.
    #대답을 생성하는 과정 자체에는 db_art와 db_etc를 모두 활용할 수 있으나, 대답에 들어갈 text는 db_art에서만 뽑아와야 할 것.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=if_dbart_only_messages + [
            {"role": "user", "content": query},
        ],
    )
    if response == "True":
        if_dbart_only = True
    else:
        if_dbart_only = False
    return if_dbart_only
''';


def get_data_from_db(query, db_art, db_etc):
    #query: user의 질문
    #db_art: art관련 db
    #db_etc: 기타 내용 관련 db

    query_embed = utils.get_embedding(query)[0].embedding
    #query_embed: query_keyword를 바탕으로 embedding을 추출 (float list)


    


    # 현재 여기까지 진행중

    index = faiss.IndexFlatL2(len(query_embed))

    db_embed = db[1]
    index.add(np.array(db_embedding))

    k = 5
    distances, indices = index.search(np.array([query_keyword]), k)

    input_string = ""
    for i in indices[i]:
        input_string += "data" + str(i + 1) + ": " + db[0][i] + "//"


# messages를 입력으로 받아, 사용자가 마지막에 보낸 내용을 맥락을 반영해 변환하고, 그 결과를 출력합니다.
# verbose=True로 설정 시 어떻게 변환됐는지 확인할 수 있습니다.
def get_clear_query(messages, verbose=False):
    prompt = get_clear_query_prompt(messages)

    clear_query = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=prompt
    ).choices[0].message.content

    if verbose:
        print(f"\nBefore: {messages[-1]['content']}")
        print(f" After: {clear_query}\n")

    return clear_query

def ask(messages):
    messages_with_clear_query = copy.deepcopy(messages)
    messages_with_clear_query[-1]['content'] = get_clear_query(messages, verbose=True)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_with_clear_query,
        stream=True
    )
    return stream