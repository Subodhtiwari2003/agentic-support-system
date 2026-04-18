from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def load_documents():
    loader = TextLoader("data/docs/faq.txt")
    documents = loader.load()

    db = Chroma.from_documents(
        documents,
        GoogleGenerativeAIEmbeddings(),
        persist_directory="data/db"
    )

    db.persist()

if __name__ == "__main__":
    load_documents()