# logics/main_logics.py

from openai import OpenAI
from prompts.main_prompts import get_clear_query_prompt
import prompts.main_prompts as main_prompts
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy

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


def artdata_to_string(data):
    """예술품 관련 data를 string 형태로 변환
    Args:
        data (dict): 예술품 관련 data
    """
    ret_str = ""
    for each_key in data.keys():
        ret_str += "[" + each_key + "]: " + data[each_key]
    return ret_str


def get_art_data_from_db(query, db_art):
    """query와 관련한 DB의 data를 검색해서 string 형태로 도출
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: 예술품 DB
    """

    query_embed = get_embedding(query)[0].embedding
    #query_embed: query_keyword를 바탕으로 embedding을 추출 (float list)
    art_idx = faiss.IndexFlatL2(len(query_embed))
    db_art_emb = [each_data[1] for each_data in db_art]
    art_idx.add(np.array(db_art_emb))
    art_dists, art_idxs = art_idx.search(np.array([query_embed]), 3)

    data_string = ""
    data_string += "예술품 관련 data 목록: ["
    for i in art_idxs[0]:
        data_string += "예술품 data" + str(i + 1) + ": " + artdata_to_string(db_art[i][0]) + "//"
    data_string += "]"

    return data_string


def get_etc_data_from_db(query, db_etc):
    """query와 관련한 DB의 data를 검색해서 string 형태로 도출
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: db_etc: 기타 DB
    """

    query_embed = get_embedding(query)[0].embedding
    #query_embed: query_keyword를 바탕으로 embedding을 추출 (float list)
    etc_idx = faiss.IndexFlatL2(len(query_embed))
    db_etc_emb = [each_data[1] for each_data in db_etc]
    etc_idx.add(np.array(db_etc_emb))
    etc_dists, etc_idxs = etc_idx.search(np.array([query_embed]), 7)

    data_string = ""
    data_string += "기타 다양한 data 목록: ["
    for i in etc_idxs[0]:
        data_string += "기타 data" + str(i + 1) + ": " + db_etc[i][0] + "//"
    data_string += "]"

    return data_string



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




def ask(messages, db_art=None, db_etc=None):
    """사용자의 질문에 대해 답하는 메인 함수
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: 예술품 DB, db_etc: 기타 DB
    """
    
    messages_with_clear_query = copy.deepcopy(messages)[:-1]
    clear_query = get_clear_query(messages, verbose=True)
    art_data_string = get_art_data_from_db(clear_query, db_art)
    etc_data_string = get_etc_data_from_db(clear_query, db_etc)

    messages_with_clear_query += [
        {"role": "system", "content": etc_data_string},
        {"role": "system", "content": art_data_string},
        {"role": "user", "content": clear_query},
        {"role": "system", "content": main_prompts.answer_based_on_data}
    ]
    #etc_data_string: 사용자 질문(가공됨)에 대한 기타 데이터를 제공.
    #art_data_string: 사용자 질문(가공됨)에 대한 예술품 관련 데이터를 제공.
    #clear_query: 사용자 질문을 지금까지의 문맥을 반영한 질문(즉, 가공됨)으로 변환해 제공.
    #answer_based_on_data: assistant의 대답을 제어하는 문장. (더 좋은 아이디어가 있으면 수정해주세요)

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_with_clear_query,
        stream=True
    )
    return stream