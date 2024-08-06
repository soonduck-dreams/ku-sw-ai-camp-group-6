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
    {"role": "system", "content": "위 user의 질문에 대해 네가 생성할 대답이 특정 작품에 대한 설명이라면, db_art의 데이터만 활용해서 대답해야 해."\
     "그렇지 않다면, db_art 및 db_etc 모두를 활용해 대답을 형성해야 해. db_art만 써야하면 True를, 둘 모두를 써야하면 False를 대답해."\
        "예시 질문1: /이중섭의 황소에 대해 알려줘/ -> (db_art의 데이터만을 써서 대답해야 함.) 대답: True"\
            "예시 질문2: /황소와 비슷한 작품을 추천해줘/ -> (db_art의 데이터만을 써서 대답해야 함.) 대답: True"\
                "예시 질문3: /이중섭의 황소에 담긴 뜻을 알려줘/ -> (db_art와 db_etc의 데이터를 모두 활용해야 함. 대답: False"\
                    "."},
]   #미사용

if_dbart_only_messages=[{'role': 'system', 'content': "user의 질문에 대해 네가 생성할 대답이 특정 작품에 대한 설명이라면, db_art의 데이터만 활용해서 대답해야 해."\
     "그렇지 않다면, db_art 및 db_etc 모두를 활용해 대답을 형성해야 해. db_art만 써야하면 True를, 둘 모두를 써야하면 False를 대답해."},
        {'role': 'user', 'content': '이중섭의 황소에 대해 알려줘'},
        {'role': 'assistant', 'content': 'True'},
        {'role': 'user', 'content': '황소와 비슷한 작품을 추천해줘'},
        {'role': 'assistant', 'content': 'True'},
        {'role': 'user', 'content': '이중섭의 황소에 담긴 뜻을 알려줘'},
        {'role': 'assistant', 'content': 'False'},]

extract_keyword_prompt = [
    {"role": "system", "content": "위 user 질문을 database에서 검색하려고 해."\
     "database는 작품에 대한 DB: [작가명, 작품명, 제작연도, 재료, 규격, 부문, 관리번호, 작품설명]"\
        "작품 외적인 DB: [작품 외적인 내용] 의 형태로 구성되어있어."\
            "user의 질문에 대해 최적의 대답을 얻어내기 위해 DATABASE에서 검색할 keyword들을 추출해봐."\
                "예시로는 /[작가명]:이중섭, [부문]:조각이 아닌 것/ 형태로 만들 수 있겠지."},
]

