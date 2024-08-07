import fitz  # PyMuPDF
import faiss
import numpy as np
from logics import main_logics
from logics.main_logics import get_embedding


def read_pdf(file_path):
    """PDF 파일을 읽어 텍스트로 변환합니다."""
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# PDF 파일 경로 설정
pdf_path = "logics/database2_v1.pdf"


def sliding_window(tokens, window_size, step_size):
    """토큰 리스트를 슬라이딩 윈도우 기법을 사용하여 청크로 나눕니다."""
    chunks = []
    for i in range(0, len(tokens) - window_size + 1, step_size):
        chunk = tokens[i:i + window_size]
        chunks.append(' '.join(chunk))
    # 마지막 청크 추가 (필요 시)
    if len(tokens) % step_size != 0 and len(tokens) > window_size:
        chunks.append(' '.join(tokens[-window_size:]))
    return chunks


documents = pdf_path

embeddings = np.array([get_embedding(doc)[0] for doc in documents if doc.strip() != ''])
