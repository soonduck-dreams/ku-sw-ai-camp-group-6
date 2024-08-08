# logics/main_logics.py

from openai import OpenAI
from prompts.main_prompts import get_clear_query_prompt
import os
from dotenv import load_dotenv
import faiss
import numpy as np
import copy
from logics.database_loader import prepare_database

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

# Load the database
db_art, db_art_emb = prepare_database('database/이중섭_김환기.csv')

def get_embedding(input):
    response = client.embeddings.create(
        input=input,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def artdata_to_string(data):
    ret_str = ""
    for each_key in data.keys():
        ret_str += "[" + each_key + "]: " + str(data[each_key]) + " "
    return ret_str

def get_data_from_db(query, db_art, db_art_emb):
    query_embed = get_embedding(query)
    art_idx = faiss.IndexFlatL2(len(query_embed))
    art_idx.add(np.array(db_art_emb))

    art_dists, art_idxs = art_idx.search(np.array([query_embed]), 3)

    data_string = "예술품 관련 data 목록: ["
    for i in art_idxs[0]:
        data_string += "예술품 data" + str(i + 1) + ": " + artdata_to_string(db_art.iloc[i]) + "//"
    data_string += "]"

    print("Retrieved Data: ", data_string)  # Print the retrieved data for the test query

    return data_string

def ask(messages):
    messages_with_clear_query = copy.deepcopy(messages)
    messages_with_clear_query[-1]['content'] = get_clear_query(messages, verbose=True)

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages_with_clear_query,
        stream=True
    )
    return stream

def get_clear_query(messages, verbose=False):
    prompt = get_clear_query_prompt(messages)

    clear_query = client.chat.completions.create(
        model="gpt-4",
        messages=prompt
    ).choices[0].message.content

    if verbose:
        print(f"\nBefore: {messages[-1]['content']}")
        print(f" After: {clear_query}\n")

    return clear_query

# Test the retrieval
test_query = "이중섭의 황소에 대해 알려줘"  # Example query
get_data_from_db(test_query, db_art, db_art_emb)
