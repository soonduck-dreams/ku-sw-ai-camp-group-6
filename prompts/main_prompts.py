import logics.util as util

'''
#미사용
if_dbart_only_messages=[{'role': 'system', 'content': "user의 질문에 대해 네가 생성할 대답이 특정 작품에 대한 설명이라면, db_art의 데이터만 활용해서 대답해야 해."\
     "그렇지 않다면, db_art 및 db_etc 모두를 활용해 대답을 형성해야 해. db_art만 써야하면 True를, 둘 모두를 써야하면 False를 대답해."},
        {'role': 'user', 'content': '이중섭의 황소에 대해 알려줘'},
        {'role': 'assistant', 'content': 'True'},
        {'role': 'user', 'content': '황소와 비슷한 작품을 추천해줘'},
        {'role': 'assistant', 'content': 'True'},
        {'role': 'user', 'content': '이중섭의 황소에 담긴 뜻을 알려줘'},
        {'role': 'assistant', 'content': 'False'},]
''';

def get_clear_query_prompt(messages):
  user_last_message = ''
  for message in messages[::-1]:
    if message['role'] == 'user':
      user_last_message = message
      break
  
  user_prefix = "Rewrite this so that pronouns and missing contexts are clarified. However, DO NOT add unnecessary information. Act as if you are the user.:"

  prompt = [
    {'role': 'system', 'content': "Your task is to clarify the user's last message based on the previous context of the conversation."},
    {'role': 'user', 'content': f'{user_prefix} 더 자세히 설명해 주세요.'},
    {'role': 'assistant', 'content': '이중섭이 왜 소를 소재로 많은 그림을 그렸는지 더 자세히 설명해 주세요.'},
    {'role': 'user', 'content': f'{user_prefix} 그의 라이벌이 있었나요?'},
    {'role': 'assistant', 'content': '알레산드로 보티첼리의 라이벌이었던 다른 화가들이 있었나요?'},
    {'role': 'user', 'content': f'{user_prefix} 좋아요'},
    {'role': 'assistant', 'content': '좋아요'},
    {'role': 'system', 'content': f'Here is the conversation history: {util.messages_to_string(messages)}'},
    {'role': 'user', 'content': f'{user_prefix} {user_last_message}'},
    ]

  return prompt

answer_based_on_data = [
  {'role': 'system', 'content': '위 유저의 질문에 대답하되, 검색된 데이터 중 상관성이 낮은 데이터는 무조건 쓰지마.'\
    '예술품 관련 data는 조금 더 신뢰도가 높은 데이터라고 생각하렴.'\
      '대답을 구어체로 해. 한 사람이 쭉 말하는 대사의 형식으로 해.'},
]