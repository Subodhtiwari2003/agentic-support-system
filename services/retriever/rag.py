from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings  # ✅ fixed

def get_vector_db():
    embedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="data/db",
        embedding_function=embedding
    )
    return db


def retrieve_docs(query: str):
    db = get_vector_db()
    return db.similarity_search(query, k=3)