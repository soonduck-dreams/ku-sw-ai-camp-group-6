query_for_db = [
    {
        'role': 'system', 'content': """
        사용자의 질문을 참고해서, embedding된 database에서 검색할 통일된 하나의 문장을 제시해봐. 네가 제시한 문제를 embedding해서 데이터베이스에서 검색할거야.
        database는 예술품 database의 경우 작품명, 작가명, 제작연도, 부문, 관리번호, 재료, 작품 설명 등이 정리되어 있어.
        기타 database의 경우 다양한 정보들이 긴 문단으로 서술되어있어.
        """
    }
]