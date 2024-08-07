def messages_to_string(messages):
  str = ""
  for item in messages:
    role = item.get('role', '')
    content = item.get('content', '')
    str += f"{role}: {content}\n"
  return str
# dictionary list 형식인 messages를, 하나의 문자열 형식으로 변환합니다.