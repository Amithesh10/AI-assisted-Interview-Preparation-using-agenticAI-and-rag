import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")
VECTOR_DIR = os.path.join(BASE_DIR, "backend", "vectordb")

documents = []

for file_name in os.listdir(KNOWLEDGE_DIR):
    file_path = os.path.join(KNOWLEDGE_DIR, file_name)

    if file_name.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

    elif file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=VECTOR_DIR
)

print("Vector Database Created Successfully")
print(f"Total Chunks: {len(chunks)}")
