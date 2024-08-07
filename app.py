# app.py

import streamlit as st
import logics.main_logics as main_logics
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
  
  stream = main_logics.ask(st.session_state.messages)
  with st.chat_message("assistant"):
     response = st.write_stream(stream)
  st.session_state.messages.append({'role': 'assistant', 'content': response})