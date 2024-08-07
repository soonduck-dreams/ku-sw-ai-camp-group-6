# app.py

import streamlit as st
import logics.main_logics as main_logics
from prompts.initial_prompts import initial_prompt
from streamlit_mic_recorder import speech_to_text
from pathlib import Path
import openai

def set_recent_modality(*args):
   data = args[0]
   st.session_state.recent_modality = data

st.title('ADY: AI Docent For You')

if "messages" not in st.session_state:
  st.session_state.messages = initial_prompt

if "recent_modality" not in st.session_state:
   st.session_state.recent_modality = None

with st.sidebar:
  text = speech_to_text(
    language='ko-KR',
    start_prompt="●",
    stop_prompt="■",
    just_once=False,
    use_container_width=True,
    callback=set_recent_modality,
    args=(['speech']),
  )

for index, message in enumerate(st.session_state.messages):
  if message["role"] != "system":
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

user_prompt = st.chat_input(
   on_submit=set_recent_modality,
   args=(['text'])
)

if user_prompt and st.session_state.recent_modality == 'text':
  st.session_state.messages.append({'role': 'user', 'content': user_prompt})
  with st.chat_message('user'):
    st.markdown(user_prompt)
  
  stream = main_logics.ask(st.session_state.messages)
  with st.chat_message("assistant"):
     response = st.write_stream(stream)
  st.session_state.messages.append({'role': 'assistant', 'content': response})
  st.session_state.recent_modality = None

if text and st.session_state.recent_modality == 'speech':
  st.session_state.messages.append({'role': 'user', 'content': text})
  with st.chat_message('user'):
    st.markdown(text)
  
  stream = main_logics.ask(st.session_state.messages)
  with st.chat_message("assistant"):
    response = st.write_stream(stream)
  st.session_state.messages.append({'role': 'assistant', 'content': response})
  speech_file_path = Path(__file__).parent / "speech.mp3"
  response = openai.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="The quick brown fox jumped over the lazy dog."
  )
  response.stream_to_file(speech_file_path)