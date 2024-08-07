# logics/example_logics.py

from openai import OpenAI
from prompts.main_prompts import get_clear_query_prompt
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)


def get_embedding(input):
    #input을 임베딩한 결과를 return하는 함수
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data


def artdata_to_string(data):
    ret_str = ""
    for each_key in data.keys():
        ret_str += "[" + each_key + "]: " + data[each_key]
    return ret_str


def get_data_from_db(query, db_art, db_etc):
    """query와 관련한 DB의 data를 검색해서 string 형태로 도출
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: 예술품 DB, db_etc: 기타 DB
    """

    query_embed = get_embedding(query)[0].embedding
    #query_embed: query_keyword를 바탕으로 embedding을 추출 (float list)

    art_idx = faiss.IndexFlatL2(len(query_embed))
    etc_idx = faiss.IndexFlatL2(len(query_embed))

    db_art_emb = db_art[1]
    db_etc_emb = db_etc[1]

    art_idx.add(np.array(db_art_emb))
    etc_idx.add(np.array(db_etc_emb))

    art_dists, art_idxs = art_idx.search(np.array([query_embed]), 3)
    etc_dists, etc_idxs = etc_idx.search(np.array([query_embed]), 7)

    data_string = ""
    data_string += "예술품 관련 data 목록: ["
    for i in art_idxs[0]:
        data_string += "예술품 data" + str(i + 1) + ": " + artdata_to_string(db_art[0][i]) + "//"
    data_string += "]"
    data_string += "기타 다양한 data 목록: ["
    for i in etc_idxs[0]:
        data_string += "기타 data" + str(i + 1) + ": " + db_etc[0][i] + "//"
    data_string += "]"

    print(data_string)      #TEST

    return data_string




def ask(messages, db_art=None, db_etc=None):
    """사용자의 질문에 대해 답하는 기본 함수
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: 예술품 DB, db_etc: 기타 DB
    """
    messages_with_clear_query = copy.deepcopy(messages)
    messages_with_clear_query[-1]['content'] = get_clear_query(messages, verbose=True)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_with_clear_query,
        stream=True
    )
    return stream

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