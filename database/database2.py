import sys
import os

# 프로젝트 루트 디렉토리를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import fitz  # PyMuPDF
import numpy as np
import nltk
from logics.main_logics import get_embedding  # get_embedding 함수가 필요합니다.

# NLTK punkt 다운로드
nltk.download('punkt')

def read_pdf(file_path):
    """PDF 파일을 읽어 텍스트로 변환합니다."""
    try:
        print(f"Attempting to open PDF file: {file_path}")
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            print(f"Reading page {page_num + 1} of {len(doc)}")
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def tokenize_text(text):
    """텍스트를 토큰으로 분할합니다."""
    return nltk.word_tokenize(text)

def sliding_window(tokens, window_size=1000, step_size=500):
    """토큰 리스트를 슬라이딩 윈도우 기법을 사용하여 청크로 나눕니다."""
    chunks = []
    for i in range(0, len(tokens), step_size):
        chunk = tokens[i:i + window_size]
        chunks.append(' '.join(chunk))
        if len(chunk) < window_size and i + window_size >= len(tokens):
            break
    return chunks


# PDF 파일 경로 설정
pdf_path = r"C:\Users\dlwns\Desktop\Junseok\python\SW_AI\ku-swaicamp-group6\database\database2_v1.pdf"

# PDF 파일 읽기
pdf_text = read_pdf(pdf_path)

# PDF 파일 읽기에 실패한 경우 종료
if not pdf_text:
    sys.exit("Failed to read PDF file. Exiting...")

# 텍스트를 토큰으로 분할
tokens = tokenize_text(pdf_text)

# 토큰을 청크로 나누기
chunks = sliding_window(tokens, window_size=1000, step_size=500)

def count_tokens(text):
    """텍스트의 총 토큰 수를 계산합니다."""
    tokens = tokenize_text(text)
    return len(tokens)

# 텍스트의 총 토큰 수 확인
total_tokens = count_tokens(pdf_text)
print(f"Total number of tokens: {total_tokens}")
