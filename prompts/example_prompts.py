# prompts/example_prompts.py

# 다양한 예시 프롬프트 정의
# 특정 task를 위한 프롬프트마다 prompts 폴더 안에서 별도의 .py 파일로 만들어서 관리하면 좋을 것 같습니다.

import logics.util as util

greeting_prompt = [
    {"role": "system", "content": "You are a helpful assistant. Speak in Korean."},
    {"role": "user", "content": "Hello! How can I assist you today?"}
]

summary_prompt = [
    {"role": "system", "content": "You are a summarization assistant."},
    {"role": "user", "content": "Summarize the following text: {text}"}
]

if_dbart_only_prompt = [
    {"role": "system", "content": "위 user의 질문에 대해 네가 생성할 대답이 특정 작품에 대한 설명이라면, db_art 에서만 data를 검색해서 대답해야 해."\
     "그렇지 않다면, db_art 및 db_etc 모두에서 data를 검색해야 해."\
        "예시 질문1: /이중섭의 황소에 대해 알려줘/ -> db_art의 검색 결과만을 보고 대답해야 함."\
            "예시 질문2: /이중섭의 황소에 담긴 뜻을 알려줘/ -> db_art와 db_etc의 검색 결과를 모두 활용해야 함."\
                "user 질문에 대한 너의 대답이 db_art만 검색해야 할 지, db_art와 db_etc를 모두 검색해야 할 지 대답해."},
]

extract_keyword_prompt = [
    {"role": "system", "content": "위 user 질문을 database에서 검색하려고 해."\
     "database는 작품에 대한 DB: [작가명, 작품명, 제작연도, 재료, 규격, 부문, 관리번호, 작품설명]"\
        "작품 외적인 DB: [작품 외적인 내용] 의 형태로 구성되어있어."\
            "user의 질문에 대해 최적의 대답을 얻어내기 위해 DATABASE에서 검색할 keyword들을 추출해봐."\
                "예시로는 /[작가명]:이중섭, [부문]:조각이 아닌 것/ 형태로 만들 수 있겠지."},
]

def get_clear_query_prompt(messages):
  user_last_message = messages[-1]['content']
  
  user_prefix = "Rewrite this so that context is clarified. Act as if you are the user. Be as faithful as the given text:"

  prompt = [
    {'role': 'system', 'content': "Your task is to clarify the user's last message based on the previous context of the conversation."},
    {'role': 'user', 'content': f'{user_prefix} 더 자세히 설명해 주세요.'},
    {'role': 'assistant', 'content': '이중섭이 왜 소를 소재로 많은 그림을 그렸는지 더 자세히 설명해 주세요.'},
    {'role': 'user', 'content': f'{user_prefix} 그의 라이벌이 있었나요?'},
    {'role': 'assistant', 'content': '알레산드로 보티첼리의 라이벌이었던 다른 화가들에 대해 알려주세요.'},
    {'role': 'user', 'content': f'{user_prefix} 그가 그런 식으로 활동하는 이유를 한 줄로 얘기하면?'},
    {'role': 'assistant', 'content': '알레산드로 보티첼리의 라이벌이었던 다른 화가들에 대해 알려주세요.'},
    {'role': 'user', 'content': f'{user_prefix} 안녕!'},
    {'role': 'assistant', 'content': '안녕!'},
    {'role': 'system', 'content': f'Here is the conversation history: {util.messages_to_string(messages)}'},
    {'role': 'user', 'content': f'{user_prefix} {user_last_message}'},
    ]

  return prompt