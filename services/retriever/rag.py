import os
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter


# Initialize embeddings with Google
embeddings = GoogleGenerativeAIEmbeddings(
    model="text-embedding-004",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Initialize the in-memory vector store
vector_store = InMemoryVectorStore(embedding=embeddings)


def load_documents():
    """Load documents from data/docs/ directory."""
    docs = []
    docs_dir = "data/docs"
    
    if not os.path.exists(docs_dir):
        print(f"Warning: {docs_dir} does not exist")
        return docs
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                docs.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return docs


def split_documents(docs):
    """Split documents into chunks."""
    text_splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return text_splitter.split_documents(docs)


def initialize_vector_store():
    """Initialize the vector store with documents from data/docs/."""
    global vector_store
    
    docs = load_documents()
    if not docs:
        print("No documents found to index")
        return
    
    chunks = split_documents(docs)
    print(f"Indexing {len(chunks)} document chunks...")
    
    vector_store.add_documents(chunks)
    print("Vector store initialized successfully")


def retrieve_docs(query: str, k: int = 3):
    """Retrieve relevant documents for a query."""
    results = vector_store.similarity_search(query, k=k)
    return results


# Initialize at module load
initialize_vector_store()