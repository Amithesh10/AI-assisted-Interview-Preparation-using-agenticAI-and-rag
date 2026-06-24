import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(BASE_DIR, "vectordb")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectordb = Chroma(
    persist_directory=VECTOR_DIR,
    embedding_function=embeddings
)

retriever = vectordb.as_retriever(search_kwargs={"k": 3})

def retrieve_context(query: str) -> str:
    try:
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant knowledge found."

        return "\n\n".join(doc.page_content for doc in docs)

    except Exception as e:
        return f"RAG retrieval error: {str(e)}"
