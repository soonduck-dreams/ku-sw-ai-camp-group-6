# app.py

import streamlit as st
import logics.main_logics as main_logics
from prompts.initial_prompts import initial_prompt

#이하는 test용 database import입니다
import example_artdata_result as ex_ad
import example_etcdata_result as ex_ed


st.title('ADY: AI Docent For You')

if "messages" not in st.session_state:
  st.session_state.messages = initial_prompt

for index, message in enumerate(st.session_state.messages):
  if message["role"] != "system":
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

user_prompt = st.chat_input()
if user_prompt:
  st.session_state.messages.append({'role': 'user', 'content': user_prompt})
  with st.chat_message('user'):
    st.markdown(user_prompt)

  #이하는 test용 database 사용입니다
  art_data = ex_ad.data
  etc_data = ex_ed.data
  
  stream = main_logics.ask(st.session_state.messages, art_data, etc_data)
  with st.chat_message("assistant"):
     response = st.write_stream(stream)
  st.session_state.messages.append({'role': 'assistant', 'content': response})