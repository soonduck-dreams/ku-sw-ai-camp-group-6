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
  {'role': 'system', 'content':
   '답변할 때 정확한 정보에 기반하여 대답해. 확인되지 않은 정보는 절대 사용하지 말고, 모르는 내용에 대해서는 \'잘 모르겠습니다\'라고 답해.'\
    '예술품 관련 data는 조금 더 신뢰도가 높은 데이터라고 생각하도록 해.'\
    '사용자의 관심사나 이전 질문을 바탕으로 맞춤형 답변을 제공해. 사용자의 취향을 고려해 더 흥미로운 정보를 제공해봐.'\
      '대답할 때, 너무 지루하지 않게 감정 표현을 풍부하게 드러내면서도 사용자에게 친근하고 전문적인 느낌을 줄 수 있도록 해.'\
      '답변은 너무 길어지지 않도록 30초 이내로 짧고 간결하게 제공하도록 해'\
      '사용자가 질문을 명확하게 이해할 수 있도록, 필요하다면 간단히 질문을 재구성하거나 구체화해'\
        '다음 질문에 답변할 때는 이전에 제공한 답변을 확인하고, 중복되지 않는 새로운 정보를 제공해줘.'\
        '긴 설명 후, 주요 포인트를 요약하고 강조해. 사용자가 핵심 정보를 놓치지 않도록 도와줘.'\
          '답변 후 사용자가 더 궁금한 점이 있는지 물어보고, 추가 질문을 유도해 사용자와의 상호작용을 높여.'},
]