# -*- coding: utf-8 -*- 

import sys
import os
import csv
import numpy as np
import nltk
import time

# Add the project root to the Python path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)

from logics.util import get_embedding

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

def embed_data(data_dict):
    """Embed the data using the embedding function and return a dictionary with embeddings."""
    embedded_data = {}
    for key, value in data_dict.items():
        text = str(value).strip('{}')
        embedding = get_embedding(text)
        embedded_data[key] = {
            'data': value,
            'embedding': embedding
        }
        print(f"Embedded data for key: {key}")
    return embedded_data

def summarize_embeddings(embedded_data_dict):
    """Summarize the embeddings to check if they were generated successfully."""
    summary = {
        'total_entries': len(embedded_data_dict),
        'embedding_lengths': [],
        'failed_embeddings': []
    }

    for key, value in embedded_data_dict.items():
        embedding = value['embedding']
        if embedding:
            summary['embedding_lengths'].append(len(embedding))
        else:
            summary['failed_embeddings'].append(key)

    average_length = np.mean(summary['embedding_lengths']) if summary['embedding_lengths'] else 0
    summary['average_embedding_length'] = average_length

    return summary

# CSV file path relative to the current file
csv_path = os.path.join(current_dir, "이중섭_김환기.csv")

# Read CSV file into a dictionary
csv_data_dict = read_csv_to_dict(csv_path)
if not csv_data_dict:
    sys.exit("Failed to read CSV file with any encoding. Exiting...")

print("CSV Data Dictionary:")
for key, value in csv_data_dict.items():
    print(f"{key}: {value}")

# Embed the data
embedded_data_dict = embed_data(csv_data_dict)

# Summarize the embedding results
embedding_summary = summarize_embeddings(embedded_data_dict)

# Print the summary
print("\nEmbedding Summary:")
print(f"Total entries: {embedding_summary['total_entries']}")
print(f"Average embedding length: {embedding_summary['average_embedding_length']}")
print(f"Failed embeddings: {embedding_summary['failed_embeddings']}")
if embedding_summary['failed_embeddings']:
    print(f"Number of failed embeddings: {len(embedding_summary['failed_embeddings'])}")
else:
    print("All embeddings generated successfully.")

# Example of accessing the embedded data
print("\nFinal Embedded Data Structure:")
embedded_data_list = []
for key, value in embedded_data_dict.items():
    embedded_data_list.append((value['data'], value['embedding'][0].embedding))


# Now you can use the `embedded_data_list` for retrieval-augmented generation (RAG) tasks

with open('./database/database1.py', 'w', encoding='UTF-8') as file:
    file.write(f"data = {embedded_data_list}")
