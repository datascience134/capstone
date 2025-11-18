# this script was run to generate the vector_db, which was then uploaded to github and used in RAG
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings

def load_documents(pdf_storage_path: str):
    pdf_directory = Path(pdf_storage_path)
    documents = []
    
    for pdf_path in pdf_directory.glob("*.pdf"):
        print(f"  Loading {pdf_path.name}...")
        loader = PyPDFLoader(str(pdf_path))
        loaded_docs = loader.load()
        documents.extend(loaded_docs)
    
    return documents

def chunk_documents(documents, chunk_size=1500, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def build_collection(embeddings_model, pdf_path, collection_name, persist_dir="./vector_db"):
    """Build a single collection"""
    print(f"\n{'='*60}")
    print(f"Building collection: {collection_name}")
    print(f"{'='*60}")
    
    # Load documents
    print(f"Loading documents from {pdf_path}...")
    docs = load_documents(pdf_path)
    print(f"✓ Loaded {len(docs)} documents")
    
    # Chunk documents
    print("Chunking documents...")
    chunked_docs = chunk_documents(docs)
    print(f"✓ Created {len(chunked_docs)} chunks")
    
    # Create collection
    print(f"Creating collection '{collection_name}'...")
    vectordb = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings_model,
        collection_name=collection_name,
        persist_directory=persist_dir
    )
    
    print(f"✓ Collection '{collection_name}' created with {vectordb._collection.count()} documents")
    return vectordb

# Initialize embeddings model
print("Initializing embeddings model...")
embeddings_model = AzureOpenAIEmbeddings(
    azure_endpoint=AZUREOPENAI_ENDPOINT,
    api_key=AZUREOPENAI_API_KEY,
    api_version=AZUREOPENAI_API_VERION,
    azure_deployment=EMBEDDING_MODEL
)
print("✓ Embeddings model ready")

# Build Collection 1: Licenses
vectordb_licenses = build_collection(
    embeddings_model=embeddings_model,
    pdf_path = "./data/licenses",
    collection_name="licenses"
)

# Build Collection 2: Local Company Setup
vectordb_localcompany = build_collection(
    embeddings_model=embeddings_model,
    pdf_path = "./data/set up local company",
    collection_name="localcompany_setup"
)

print(f"\n{'='*60}")
print("✅ All collections built successfully!")
print(f"{'='*60}")
print(f"Collection 'licenses': {vectordb_licenses._collection.count()} documents")
print(f"Collection 'localcompany_setup': {vectordb_localcompany._collection.count()} documents")