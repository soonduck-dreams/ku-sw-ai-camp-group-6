import openai
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

def set_recent_modality(*args):
   data = args[0]
   state = args[1]
   state.recent_modality = data

def text_to_speech(text, speech_file_path):
  with openai.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="nova",
    input=text,
    speed=1
  ) as response_speech:
    response_speech.stream_to_file(speech_file_path)

def get_user_intent(text):
  user_intent = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {'role': 'system', 'content': '사용자의 말을 다음 중 하나로 분류하라: 일상적 대화, 감상 중인 작품 밝히기, 감상 중인 그림에 대한 직접적 질문, 감상 중인 그림에 대한 간접적 질문, 추천 요청'},
      {'role': 'user', 'content': '안녕!'},
      {'role': 'assistant', 'content': '일상적 대화'},
      {'role': 'user', 'content': '그림이 너무 예쁘다.'},
      {'role': 'assistant', 'content': '일상적 대화'},
      {'role': 'user', 'content': '도슨트로 일한 지 얼마나 됐어?'},
      {'role': 'assistant', 'content': '일상적 대화'},
      {'role': 'user', 'content': '나는 지금 반 고흐의 해바라기를 보고 있어'},
      {'role': 'assistant', 'content': '감상 중인 작품 밝히기'},
      {'role': 'user', 'content': '이 작품에서 황소가 무슨 표정을 짓고 있는 거야?'},
      {'role': 'assistant', 'content': '감상 중인 그림에 대한 직접적 질문'},
      {'role': 'user', 'content': '이 그림을 구매한 이건희의 수집 철학에 대해 알고 있니?'},
      {'role': 'assistant', 'content': '감상 중인 그림에 대한 간접적 질문'},
      {'role': 'user', 'content': '같은 시대의 다른 작가를 추천해줘.'},
      {'role': 'assistant', 'content': '추천 요청'},
      {'role': 'user', 'content': text}
    ]
  ).choices[0].message.content

  print(user_intent)

  system_message = ''

  if user_intent == '일상적 대화':
    system_message = '사용자가 일상적 대화를 하고 있다. 사용자와 감정을 공유하며, 장난스럽게 다가가라. 사용자가 미술 작품 감상과 관련 없는 이야기를 한다면, 너가 AI 도슨트라는 걸 상기시키고 장난스럽게 혼내라.'
  elif user_intent == '감상 중인 작품 밝히기':
    system_message = '사용자가 감상 중인 작품이 무엇인지 말하고 있다. 그 작품의 작가, 제작 시기, 사용 재료를 간단히 언급하라. 잠시 감상할 시간을 주어라.'
  elif user_intent == '감상 중인 그림에 대한 직접적 질문':
    system_message = '사용자가 감상 중인 작품에 대해 질문하고 있다. 질문 내용에 답하라. 필요하다면 사용자가 작품의 특정 부분에 집중하도록 유도해라 e.g. 그림의 왼쪽 위를 봐볼래?, 사진의 오른쪽 끝에 웅크려 앉아 있는 남자가 보이니?\nFormat: less than 8 sentences'
  elif user_intent == '감상 중인 그림에 대한 간접적 질문':
    system_message = '사용자가 감상 중인 작품과 관련한 간접적 질문을 하고 있다. 질문 내용에 답하라. 필요하다면 사용자가 감상 중인 작품에서 특정 부분에 집중하도록 유도해라. e.g. 이중섭은 소라는 생물에 자기 자신을 투영하기도 했어. 그 점을 느끼면서, 다시 한 번 작품 속 황소를 바라보면 어때?, 그림의 가운데를 보면 예수님이 있지? 그가 주위의 제자들에게 이렇게 말한 거야. "너희 가운데 하나가, 나를 배반할 것이다!"'
  elif user_intent == '추천 요청':
    system_message = '사용자가 다른 작품 또는 작가에 대해 추천해달라고 요청한다. 좀 고민하는 척 하다가, 가장 최고인 것을 1개만 추천해 주어라. 무엇을 추천하는지만 말하고, 그 이유는 말하지 마라.'
  else:
    pass
  
  return system_message