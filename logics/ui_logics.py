import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import prompts.main_prompts as main_prompts
import random
import streamlit as st

load_dotenv()
# openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_key = st.secrets['OPENAI_API_KEY']

client = OpenAI(api_key=openai_api_key)

def set_recent_modality(*args):
   data = args[0]
   state = args[1]
   state.recent_modality = data

def text_to_speech(text, speech_file_path, maltoo_option=0):
  voices = ['nova', 'nova', 'nova']
  laughs = ['헤헤', '우후후!', '에헤헤']
  between_paragraphs = [', 네, 그리고 그리고...', '아이고, 잠시 숨 좀 고를게요.', '자~! 이게 다가 아니죠!']

  if maltoo_option == 0:
    text = text.replace('!', '~~~~~!!!')
    text = text.replace('?', f'~~~~~? {laughs[random.randrange(len(laughs))]}, ')
    text = text.replace('.', '~~~~~!!! ...')
    text = text.replace('AI 도슨트', 'AI~~! 도슨트')
    text = text.replace('*', '~~')
    text = text.replace('😊', laughs[random.randrange(len(laughs))])
    text = text.replace('✨', '으음.')
    text = text.replace('\n\n', between_paragraphs[random.randrange(len(between_paragraphs))])
  elif maltoo_option == 1:
    text = text.replace('.', '... 음... ')
    text = text.replace('?', f'.....? 어.....')
    text = text.replace('AI 도슨트', '에이아이 도슨트?')
    text = text.replace('\n\n', '... 어디 보자...')
    text = text.replace('*', '.....')
  elif maltoo_option == 2:
    text = text.replace('!', '~~! Wow!')
    text = text.replace('?', 'You know?')
    text = text.replace(' ', '')

  with openai.audio.speech.with_streaming_response.create(
    model="tts-1-hd",
    voice=voices[maltoo_option],
    input=text,
    speed=1
  ) as response_speech:
    response_speech.stream_to_file(speech_file_path)

def get_user_intent(text):
  intent_list = ['일상적 대화', '감상 중인 작품 밝히기', '감상 중인 작품 관련 질문', '다른 작가 또는 작품에 대한 추천 요청']
  prompt = main_prompts.get_user_intent_prompt(text, intent_list)

  user_intent = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=prompt
  ).choices[0].message.content

  os.system('cls' if os.name == 'nt' else 'clear')
  print("사용자의 말은 다음으로 분류됩니다: ", user_intent)

  system_message = 'Stick to the following answer policy:\n\n'
  is_RAG_required = False

  user_intent_list = user_intent.split(', ')

  if '일상적 대화' in user_intent_list:
    system_message += '사용자가 일상적 대화를 하고 있다. 사용자와 감정을 공유하며, 장난스럽게 다가가라. 사용자가 미술 작품 감상과 관련 없는 이야기를 한다면, 너가 AI 도슨트라는 걸 상기시키고 장난스럽게 혼내라.\n'
    is_RAG_required = False
  if '감상 중인 작품 밝히기' in user_intent_list:
    system_message += '사용자가 감상 중인 작품이 무엇인지 말하고 있다. 그 작품의 작가명, 제작연도, 사용 재료를 간단히 언급하라. 작품을 간단히 설명하라. 필요하다면 사용자가 작품의 특정 부분에 집중하도록 유도해라 e.g. 그림의 왼쪽 위를 봐볼래? 마지막으로, 잠시 감상할 시간을 주어라. DO NOT say the size of the artwork.\n'
    is_RAG_required = True
  if '감상 중인 작품 관련 질문' in user_intent_list:
    system_message += '사용자가 감상 중인 작품과 관련해 질문하고 있다. 질문 내용에 답하라. 필요하다면 사용자가 작품의 특정 부분에 집중하도록 유도해라 e.g. 그림의 왼쪽 위를 봐볼래?, 사진의 오른쪽 끝에 웅크려 앉아 있는 남자가 보이니? 이중섭은 소라는 생물에 자기 자신을 투영하기도 했어. 그 점을 느끼면서, 다시 한 번 작품 속 황소를 바라보면 어때?, 그림의 가운데를 보면 예수님이 있지? 그가 주위의 제자들에게 이렇게 말한 거야. "너희 가운데 하나가, 나를 배반할 것이다!"\n'
    is_RAG_required = True
  if '다른 작가 또는 작품에 대한 추천 요청' in user_intent_list:
    system_message += '사용자가 다른 작품 또는 작가에 대해 추천해달라고 요청한다. Make a recommendation from the following artworks on display.\n'
    is_RAG_required = True
  else:
    system_message += 'DO NOT make a recommendation of other artworks. Just focus on the artwork the user is appreciating at the moment.\n'

  system_message += 'DO NOT list items using "첫째, 둘째" etc. Instead, say it concisely in one sentence.\nFormat: less than 6 sentences'
  
  return {"system_message": system_message,
          "is_RAG_required": is_RAG_required}