# Retrieval Augmented Generation

This lesson shows how to load sample threat intelligence reports (reports folder) to a vector database (FAISS)
and then use the RAG pattern to fetch content to answer questions related to threat data.

## Creating the Vector Database
create_vector_db.py takes all the reports in the reports folder, chunks them, converts to embedding and save
to the FAISS database. The vector database is saved to the file rag_index.faiss and the actual chunks are
saved to rag_chunks.json.


You don't need to run this as it is already saved unless you want to add new threat intel reports (save them to
reports folder)

## RAG Agent
RAG is implemented as an MCP tool (uses studio transport for dev). When the agent is executed the following steps are followed:

- Create an embedding based on the user query
- Fetch the top N results from the RAG database
- Fill in the agent's contexts with the retrieved content
- Agent finally answers the query based on the data in the context

## Running the agent
```
adk web
```
