# app.py

import streamlit as st
from logics.example_logics import get_greeting, summarize_text
from prompts.initial_prompts import initial_prompt

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
  
  # TODO: 모델한테 메시지 보내고 받아서 표시하는 거 추가하기