# prompts/example_prompts.py

# 다양한 예시 프롬프트 정의
# 특정 task를 위한 프롬프트마다 prompts 폴더 안에서 별도의 .py 파일로 만들어서 관리하면 좋을 것 같습니다.
greeting_prompt = [
    {"role": "system", "content": "You are a helpful assistant. Speak in Korean."},
    {"role": "user", "content": "Hello! How can I assist you today?"}
]

summary_prompt = [
    {"role": "system", "content": "You are a summarization assistant."},
    {"role": "user", "content": "Summarize the following text: {text}"}
]

if_dbart_only_prompt = [
    {"role": "system", "content": "네가 생성할 대답이 특정 작품에 대한 설명이라면, db_art."},
]