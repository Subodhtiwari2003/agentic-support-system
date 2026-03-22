from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

def load_documents():
    loader = TextLoader("data/docs/faq.txt")
    documents = loader.load()

    db = Chroma.from_documents(
        documents,
        OpenAIEmbeddings(),
        persist_directory="data/db"
    )

    db.persist()

if __name__ == "__main__":
    load_documents()