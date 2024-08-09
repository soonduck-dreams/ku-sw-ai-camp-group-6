# logics/main_logics.py

from openai import OpenAI
from prompts.main_prompts import get_clear_query_prompt
from prompts.maltoo_prompts import get_maltoo_prompt
import prompts.main_prompts as main_prompts
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy
from logics.util import get_embedding, messages_to_string, print_messages_to_string
import streamlit as st


#이하는 test용 database import입니다
import utils.example_artdata_result as ex1
import utils.example_etcdata_result as ex2

import database.database2 as db2
import database.database1 as db1
art_data = db1.data
etc_data = db2.data



load_dotenv()
# openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_key = st.secrets['OPENAI_API_KEY']

client = OpenAI(api_key=openai_api_key)



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
    
    data_string = main_prompts.make_db_art_to_string(db_art, art_idxs)
    
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
    
    data_string = main_prompts.make_db_etc_to_string(db_etc, etc_idxs)

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
        print(f"\nBefore: {messages[get_user_last_message_index(messages)]['content']}")
        print(f" After: {clear_query}\n")

    return clear_query






def ask(messages, use_stream=False, use_RAG=False, maltoo_option=0):
    """사용자의 질문에 대해 답하는 메인 함수
    Args:
        messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
        db_art: 예술품 DB, db_etc: 기타 DB
    """

    messages_with_clear_query = copy.deepcopy(messages)
    user_last_message_index = get_user_last_message_index(messages_with_clear_query)
    clear_query = get_clear_query(messages)
    messages_with_clear_query[user_last_message_index]['content'] = clear_query
    
    if use_RAG:
        db_art = art_data
        db_etc = etc_data
        
        art_data_string = get_art_data_from_db(clear_query, db_art)
        etc_data_string = get_etc_data_from_db(clear_query, db_etc)
        messages_with_clear_query += ([
            {"role": "system", "content": etc_data_string},
            {"role": "system", "content": art_data_string},
        ])
        #etc_data_string: 사용자 질문(가공됨)에 대한 기타 데이터를 제공.
        #art_data_string: 사용자 질문(가공됨)에 대한 예술품 관련 데이터를 제공.
        #clear_query: 사용자 질문을 지금까지의 문맥을 반영한 질문(즉, 가공됨)으로 변환해 제공.

    messages_with_clear_query += get_maltoo_prompt(maltoo_option)

    messages_with_clear_query = move_to_end(messages_with_clear_query, user_last_message_index)

    print_messages_to_string(messages_with_clear_query, interval=0.25)

    if use_stream:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_clear_query,
            stream=True
        )
        return stream
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_clear_query,
        ).choices[0].message.content
        return response


def get_user_last_message_index(messages):
    user_last_message_index = -1
    for index, message in enumerate(messages[::-1]):
        if message['role'] == 'user':
            user_last_message_index = len(messages) - 1 - index
            break
    return user_last_message_index


def move_to_end(lst, index):
    """
    리스트에서 특정 인덱스의 요소를 마지막 위치로 옮기는 함수.

    Parameters:
    lst (list): 요소를 옮길 리스트
    index (int): 마지막 위치로 옮길 요소의 인덱스

    Returns:
    list: 요소가 마지막 위치로 옮겨진 리스트
    """
    # 요소를 마지막 위치로 옮기기
    lst.append(lst.pop(index))
    return lst