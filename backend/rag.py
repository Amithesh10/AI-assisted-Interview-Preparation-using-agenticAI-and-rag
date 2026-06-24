def retrieve_context(query, knowledge_text, top_k=4):
    """
    Lightweight RAG-style context retrieval.

    Since Groq does not provide embeddings directly here,
    we pass the uploaded/typewritten knowledge base content
    directly to the LLM as context.

    This avoids Gemini quota issues and works well for deployment.
    """

    if not knowledge_text or not str(knowledge_text).strip():
        return "No knowledge base provided."

    knowledge_text = str(knowledge_text).strip()

    return knowledge_text[:4000]
