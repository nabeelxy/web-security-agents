from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
from pathlib import Path
import json
import os
import numpy as np
import faiss
from google import genai

# Read each threat report and create document chunks with metadata
all_splits = []
for filename in glob.glob(os.path.join(os.path.dirname(__file__,), "reports/*.txt")):
    chunk_size = 1200
    chunk_overlap = 300
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    with open(filename, 'r', encoding='utf-8') as rpt:
        file_content = rpt.read()
        splits = text_splitter.split_text(file_content)

    basename = Path(filename).stem
    index = 0
    for split in splits:
        all_splits.append(json.dumps({
            'text': split,
            'source': basename,
            'chunk_index': index
        }))
        index += 1

# Create embedding for each chunk
client = genai.Client(api_key=os.envi.get('GOOGLE_API_KEY'))
all_splits_results = client.models.embed_content(
        model="gemini-embedding-001",
        contents= all_splits)

embeddings = []
for embedding in all_splits_results.embeddings:
    embeddings.append(embedding.values)

# Create FAISS index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save for future use
faiss.write_index(index, os.path.join(os.path.dirname(__file__,), "rag_index.faiss"))
with open(os.path.join(os.path.dirname(__file__,), "rag_chunks.json"), "w") as f:
    json.dump(all_splits, f)