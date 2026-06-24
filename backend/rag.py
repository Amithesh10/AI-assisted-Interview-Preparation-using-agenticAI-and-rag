import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(BASE_DIR, "vectordb")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=VECTOR_DIR,
    embedding_function=embeddings
)

retriever = vectordb.as_retriever(
    search_kwargs={"k": 4}
)

def retrieve_context(query: str) -> str:
    try:
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant knowledge found."

        return "\n\n".join([doc.page_content for doc in docs])

    except Exception as e:
        return f"RAG retrieval error: {str(e)}"
