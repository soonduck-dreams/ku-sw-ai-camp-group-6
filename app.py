# app.py

import streamlit as st
import logics.main_logics as main_logics
import logics.ui_logics as ui_logics
from prompts.initial_prompts import initial_prompt
from prompts.maltoo_prompts import get_maltoo_prompt
from streamlit_mic_recorder import speech_to_text
from pathlib import Path
import time
import copy
import os

os.system('cls' if os.name == 'nt' else 'clear')

with st.sidebar:
  st.title('ADY: AI Docent For You')

  text_from_speech = speech_to_text(
    language='ko-KR',
    start_prompt="●",
    stop_prompt="■",
    use_container_width=True,
    callback=ui_logics.set_recent_modality,
    args=(['speech', st.session_state]),
  )

  if st.button("대화 다시 시작하기", use_container_width=True):
    st.session_state['messages'] = []
    time.sleep(1)
    st.rerun()

  options = ("밝고 발랄해요",
     "긴장해서 말을 더듬어요",
     "과격하고 시끄러워요")
  maltoo_select = st.selectbox(
    "아디는 지금...",
    options,
     index=0 if "maltoo_option" not in st.session_state else st.session_state.maltoo_option
  )
  st.session_state.maltoo_option = options.index(maltoo_select)

if "maltoo_option" not in st.session_state:
  st.session_state.maltoo_option = 0

if "messages" in st.session_state:
  for index, message in enumerate(st.session_state.messages):
    if message['role'] != 'system' and index >= len(initial_prompt):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 맨 처음 ADY가 말을 건다
if "messages" not in st.session_state or not st.session_state.messages:
  st.session_state.recent_modality = None
  st.session_state.messages = copy.deepcopy(initial_prompt)
  response = main_logics.ask(st.session_state.messages, maltoo_option=st.session_state.maltoo_option)
  st.session_state.messages.append({'role': 'assistant', 'content': response})

  speech_file_path = Path(__file__).parent / "speech.mp3"
  ui_logics.text_to_speech(response, speech_file_path, st.session_state.maltoo_option)
  with st.chat_message('assistant'):
    st.markdown(response.replace('~', '~!'))
  st.audio(str(speech_file_path), autoplay=True)

if "recent_modality" not in st.session_state:
   st.session_state.recent_modality = None

user_prompt = st.chat_input(
   on_submit=ui_logics.set_recent_modality,
   args=(['text', st.session_state])
)

# 사용자의 텍스트 입력에 답하기
if user_prompt and st.session_state.recent_modality == 'text':
  st.session_state.messages.append({'role': 'user', 'content': user_prompt})
  clear_query = main_logics.get_clear_query(st.session_state.messages)
  user_intent = ui_logics.get_user_intent(clear_query)
  messages_with_system_message = copy.deepcopy(st.session_state.messages)
  messages_with_system_message.append({'role': 'system', 'content': user_intent['system_message']})
  with st.chat_message('user'):
    st.markdown(user_prompt)
  
  response = main_logics.ask(messages_with_system_message, use_RAG=user_intent['is_RAG_required'], maltoo_option=st.session_state.maltoo_option)
  st.session_state.messages.append({'role': 'assistant', 'content': response})
  st.session_state.recent_modality = None

  speech_file_path = Path(__file__).parent / "speech.mp3"
  ui_logics.text_to_speech(response, speech_file_path, st.session_state.maltoo_option)
  with st.chat_message('assistant'):
    st.markdown(response.replace('~', '~!'))
  st.audio(str(speech_file_path), autoplay=True)


# 사용자의 음성 입력에 답하기
if text_from_speech and st.session_state.recent_modality == 'speech':
  st.session_state.messages.append({'role': 'user', 'content': text_from_speech})
  clear_query = main_logics.get_clear_query(st.session_state.messages)
  user_intent = ui_logics.get_user_intent(clear_query)
  messages_with_system_message = copy.deepcopy(st.session_state.messages)
  messages_with_system_message.append({'role': 'system', 'content': user_intent['system_message']})
  with st.chat_message('user'):
    st.markdown(text_from_speech)
  
  response = main_logics.ask(messages_with_system_message, use_RAG=user_intent['is_RAG_required'], maltoo_option=st.session_state.maltoo_option)
  st.session_state.messages.append({'role': 'assistant', 'content': response})
  st.session_state.recent_modality = None

  speech_file_path = Path(__file__).parent / "speech.mp3"
  ui_logics.text_to_speech(response, speech_file_path, st.session_state.maltoo_option)
  with st.chat_message('assistant'):
    st.markdown(response.replace('~', '~!'))
  st.audio(str(speech_file_path), autoplay=True)
