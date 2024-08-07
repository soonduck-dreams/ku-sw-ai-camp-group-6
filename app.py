# app.py

import streamlit as st
from logics.example_logics import get_greeting, summarize_text, ask
from logics.example_logics import get_greeting, summarize_text, ask
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
  
  stream = ask(st.session_state.messages)
  with st.chat_message("assistant"):
     response = st.write_stream(stream)
  st.session_state.messages.append({'role': 'assistant', 'content': response})

reset_messages_button = st.button("대화 처음부터 시작")
if reset_messages_button:
   del st.session_state['messages']
   st.rerun()