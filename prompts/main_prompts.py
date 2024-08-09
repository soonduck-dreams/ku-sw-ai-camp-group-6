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
'''

def artdata_to_string(data):
    """예술품 관련 data를 string 형태로 변환
    Args:
        data (dict): 예술품 관련 data
    """
    ret_str = ""
    for each_key in data.keys():
        ret_str += each_key + ": " + data[each_key] + '\n'
    return ret_str


def make_db_art_to_string(db_art, art_idxs):
    data_string = ""
    data_string += "You can use the following artworks on display to answer to user: \n\n"
    for i in art_idxs[0]:
        data_string += artdata_to_string(db_art[i][0]) + "\n\n"
    
    return data_string
  
  
  
def make_db_etc_to_string(db_etc, etc_idxs):
    data_string = "You can use the following website search results to answer to user: \n\n"
    for i in etc_idxs[0]:
        data_string += db_etc[i][0] + "\n\n"
    
    return data_string
  


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
   ''},
]

def get_user_intent_prompt(text, intent_list):
  intent_list = ' '.join(intent_list)
  prompt = [
      {'role': 'system', 'content': f'사용자의 말을 다음 중 1개 이상으로 분류하라: {intent_list}\nFormat: comma-separated values'},
      {'role': 'user', 'content': '안녕! 나는 지금 이중섭의 황소를 보고 있어.'},
      {'role': 'assistant', 'content': '일상적 대화, 감상 중인 작품 밝히기'},
      {'role': 'user', 'content': '오늘 국립현대미술관에 왔어.'},
      {'role': 'assistant', 'content': '일상적 대화'},
      {'role': 'user', 'content': '나는 지금 반 고흐의 해바라기를 보고 있어'},
      {'role': 'assistant', 'content': '감상 중인 작품 밝히기'},
      {'role': 'user', 'content': '이 그림을 구매한 이건희의 수집 철학에 대해 알고 있니?'},
      {'role': 'assistant', 'content': '감상 중인 작품 관련 질문'},
      {'role': 'user', 'content': '이건희 컬렉션 내에서 일제강점기 영향을 받은 다른 작가는 누가 있고 대표작품은 뭐야?'},
      {'role': 'assistant', 'content': '다른 작가 또는 작품에 대한 추천 요청'},
      {'role': 'user', 'content': '이중섭이 소를 즐겨 그리게 된 배경은 뭐야? 이건희 컬렉션 내에 소가 등장하는 다른 작품도 소개해줘'},
      {'role': 'assistant', 'content': '감상 중인 작품 관련 질문, 다른 작가 또는 작품에 대한 추천 요청'},
      {'role': 'user', 'content': text}
    ]
  return prompt