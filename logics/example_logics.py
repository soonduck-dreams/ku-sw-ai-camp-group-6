# logics/example_logics.py

from openai import OpenAI
from prompts import example_prompts
from prompts.example_prompts import greeting_prompt, summary_prompt, if_dbart_only_prompt, extract_keyword_prompt
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


def get_embedding(input):
    #input을 임베딩한 결과를 return하는 함수
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data


def get_data_from_db(query, db):
    query_embed = get_embedding(query)[0].embedding


def extract_keyword(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"user": "user", "content": text},
            {"role": "system", "content": extract_keyword_prompt}
        ]
    )
    return response


def get_data_from_db_tuned(query, db):
    query_embed
    response = client.embeddings.create(
        input=input,
        model="text-embedding-3-small"
    )
    return response.data
    
    query_embed = get_embedding(query)[0].embedding

    index = faiss.IndexFlatL2(len(news_data[0][1]))

    datalist = []
    for each_data in news_data:
        datalist.append(each_data[1])
    index.add(np.array(datalist))

    k = 7
    distances, indices = index.search(np.array([query_embed]), k)

    input_news_data = ""
    for i in indices[0]:
        input_news_data += "[TITLE]: " + news_data[i][0]['title']
        input_news_data += "[HILIGHT]: " + news_data[i][0]['hilight'] + "//"

    system_message = "user의 앞선 질문에 대한 최신 뉴스 7종에 대한 검색은 다음과 같음."\
    "질문과 상관성이 부족한 검색 결과가 있을 경우 대답에 활용하지 말 것.: " + input_news_data

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": query},
            {"role": "system", "content": system_message}
        ],
        #stream=True,
    )

    #response = st.write_stream(stream)
    
    st.text_area("[Answer]", value=stream.choices[0].message.content, height=500)


def answer_art(messages, ask, db_art, db_etc):
    #사용자의 질문에 대해 답하는 기본 함수
    #messages: 지금껏 주고받은 message 기록 ex)st.session_state.messages
    #ask: 사용자의 질문
    #db_art: 예술품 DB, db_etc: 기타 DB
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]} for m in messages
        ]
        + [
            {"user": "user", "content": ask},
            #{"role": "system", "content": system_message}
        ]
    )
    return response