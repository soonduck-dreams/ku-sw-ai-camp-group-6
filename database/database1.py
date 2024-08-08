import sys
import os
import csv
import numpy as np
import nltk

# Add the project root to the Python path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from logics.main_logics import get_embedding

# Ensure nltk punkt tokenizer is available
nltk.download('punkt')

def read_csv_to_dict(file_path):
    """Read CSV file and return its content as a dictionary with '작품명' as keys."""
    encodings = ['utf-8', 'euc-kr', 'cp949']
    for encoding in encodings:
        try:
            print(f"Attempting to open CSV file: {file_path} with encoding: {encoding}")
            with open(file_path, newline='', encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                data = {row['작품명']: row for row in reader}
            print(f"CSV data successfully read with encoding {encoding}. Number of entries: {len(data)}")
            return data
        except Exception as e:
            print(f"Error reading CSV file with encoding {encoding}: {e}")
    return {}

def tokenize_text(text):
    """Tokenize text into words."""
    return nltk.word_tokenize(text)

def sliding_window(tokens, window_size=1000, step_size=500):
    """Chunk tokens using a sliding window approach."""
    chunks = []
    for i in range(0, len(tokens), step_size):
        chunk = tokens[i:i + window_size]
        chunks.append(' '.join(chunk))
        if len(chunk) < window_size and i + window_size >= len(tokens):
            break
    return chunks

# CSV file path relative to the current file
csv_path = os.path.join(current_dir, "이중섭_김환기.csv")

# Read CSV file into a dictionary
csv_data_dict = read_csv_to_dict(csv_path)
if not csv_data_dict:
    sys.exit("Failed to read CSV file with any encoding. Exiting...")

print("CSV Data Dictionary:")
for key, value in csv_data_dict.items():
    print(f"{key}: {value}")
    

# Concatenate all descriptions into a single text if chunking is needed
all_text = ' '.join([' '.join(value.values()) for value in csv_data_dict.values()])
print("All Text:")
print(all_text[:1000])  # Print first 1000 characters for brevity

# Tokenize and chunk if necessary
tokens = tokenize_text(all_text)
print("Tokens:")
print(tokens[:100])  # Print first 100 tokens for brevity

chunks = sliding_window(tokens, window_size=1000, step_size=500)
print("Chunks:")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:200]}")  # Print first 200 characters of each chunk for brevity

def count_tokens(text):
    """Count total number of tokens in text."""
    tokens = tokenize_text(text)
    return len(tokens)

# Check total number of tokens
total_tokens = count_tokens(all_text)
print(f"Total number of tokens: {total_tokens}")

# Now you can use the `chunks` for embedding or any other RAG-related processing.
