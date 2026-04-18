import os
import logging
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

logger = logging.getLogger(__name__)

# Lazy initialization - store is None until first use
vector_store = None


def get_embeddings():
    """Get Google embeddings instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    return GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",
        google_api_key=api_key
    )


def load_documents():
    """Load documents from data/docs/ directory."""
    docs = []
    docs_dir = "data/docs"
    
    if not os.path.exists(docs_dir):
        logger.warning(f"Warning: {docs_dir} does not exist")
        return docs
    
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                docs.extend(loader.load())
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
    
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
    
    if vector_store is not None:
        return  # Already initialized
    
    try:
        embeddings = get_embeddings()
        vector_store = InMemoryVectorStore(embedding=embeddings)
        
        docs = load_documents()
        if not docs:
            logger.warning("No documents found to index")
            return
        
        chunks = split_documents(docs)
        logger.info(f"Indexing {len(chunks)} document chunks...")
        
        vector_store.add_documents(chunks)
        logger.info("Vector store initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        vector_store = None


def retrieve_docs(query: str, k: int = 3):
    """Retrieve relevant documents for a query."""
    # Lazy initialization on first use
    if vector_store is None:
        initialize_vector_store()
    
    if vector_store is None:
        logger.warning("Vector store not available, returning empty results")
        return []
    
    results = vector_store.similarity_search(query, k=k)
    return results