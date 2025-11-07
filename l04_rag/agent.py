from google.adk.agents import LlmAgent
import faiss
from google import genai
import numpy as np
import json
import os

def get_embedding(text):
    client = genai.Client()#api_key=os.environ.get('GOOGLE_API_KEY'))

    result = client.models.embed_content(
            model="gemini-embedding-001",
            contents= [
                text
            ])
    return np.array(result.embeddings[0].values)

def retrieval_augmented_generation(query: str, top_k: int =5):
    """
    For a given query, retrieve relevant chunks from a vector database
    which is a pre-computed embedding index. Each returned chunk has the
    following information: text itself, source and chunk index in the source.

    Args:
        query (str): Search query text
        top_k (int, optional): Number of top similar chunks to retrieve. Defaults to 5.
    Returns:
        list: Top K most relevant text chunks based on semantic similarity
    """
    index = faiss.read_index(os.path.join(os.path.dirname(__file__,), "rag_index.faiss"))
    with open(os.path.join(os.path.dirname(__file__,), "rag_chunks.json"), "r") as f:
        chunks = json.load(f)
    
    query_vec = get_embedding(query)
    distances, indices = index.search(np.array([query_vec]), top_k)
    
    return [chunks[i] for i in indices[0]]

root_agent = LlmAgent(
    name="agent_01_rag",
    model="gemini-2.0-flash",
    description="""
        Web security analyst. 
        """,
    instruction="""
        You are an expert web security analysis agent.
        You may use the retrieval_augmented_generation tool
        to fetch relevant chunks of information from the 
        threat reports indexed locally.
        """,
    tools=[retrieval_augmented_generation]
)
