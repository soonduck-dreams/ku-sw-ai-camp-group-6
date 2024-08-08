import sys
import os

# 프로젝트 루트 디렉토리를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fitz  # PyMuPDF
import numpy as np
from logics.main_logics import get_embedding  # get_embedding 함수가 필요합니다.

def read_pdf(file_path):
    """PDF 파일을 읽어 텍스트로 변환합니다."""
    try:
        print(f"Attempting to open PDF file: {file_path}")
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            print(f"Reading page {page_num + 1} of {len(doc)}")
            page = doc.load_page(page_num)
            page_text = page.get_text()
            print(f"Page {page_num + 1} text length: {len(page_text)}")
            text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def sliding_window(text, window_size=1000, step_size=500):
    """텍스트를 슬라이딩 윈도우 기법을 사용하여 청크로 나눕니다."""
    chunks = []
    for i in range(0, len(text), step_size):
        chunk = text[i:i + window_size]
        chunks.append(chunk)
        if len(chunk) < window_size and i + window_size >= len(text):
            break
    return chunks

# PDF 파일 경로 설정
pdf_path = "database\database2_v1.pdf"

# PDF 파일 읽기
pdf_text = read_pdf(pdf_path)

# PDF 파일 읽기에 실패한 경우 종료
if not pdf_text:
    sys.exit("Failed to read PDF file. Exiting...")

# 텍스트 슬라이딩 윈도우로 나누기
chunks = sliding_window(pdf_text, window_size=1000, step_size=500)

# 각 청크에 대해 임베딩 생성 및 (chunk, embedding) 튜플 리스트 생성 호출명 chunk_embedding_list임
chunk_embedding_list = []
for idx, chunk in enumerate(chunks, start=1):
    embedding = get_embedding(chunk)[0]
    chunk_embedding_list.append((chunk, embedding))


# 결과 출력
print(f"Number of chunks: {len(chunk_embedding_list)}")
print(f"First chunk and embedding: {chunk_embedding_list}")
