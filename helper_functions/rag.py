import streamlit as st
from pathlib import Path

from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

from openai import AzureOpenAI
from helper_functions import constants

@st.cache_resource
def load_llm():
    llm = AzureChatOpenAI(
        azure_endpoint=constants.AZUREOPENAI_ENDPOINT,
        api_key=constants.AZUREOPENAI_API_KEY,
        api_version=constants.AZUREOPENAI_API_VERION,
        deployment_name=constants.AZUREOPENAI_MODEL,  # Note: deployment_name, not azure_deployment
        temperature=0,
        model_kwargs={"seed": 42}  # seed goes in model_kwargs
    )
    return llm

@st.cache_resource
def load_emb_model():
    embeddings_model = AzureOpenAIEmbeddings(
        azure_endpoint=constants.AZUREOPENAI_ENDPOINT,
        api_key=constants.AZUREOPENAI_API_KEY,
        api_version=constants.AZUREOPENAI_API_VERION,
        azure_deployment=constants.EMBEDDING_MODEL  # Your embedding deployment name
    )
    return embeddings_model

def load_documents(pdf_storage_path: str):
    """
    Load PDF documents from the given directory.
    
    :param pdf_storage_path (str): Path to the directory containing PDF documents.
    :return: A list of Document objects.
    """

    pdf_directory = Path(pdf_storage_path)
    documents = []

    # Load all PDFs
    for pdf_path in pdf_directory.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        loaded_docs = loader.load()   # returns List[Document]
        documents.extend(loaded_docs)

    return documents

def chunk_documents(documents, chunk_size=1500, chunk_overlap=100):

    # While our document is not too long, we can still split it into smaller chunks
    # This is to ensure that we can process the document in smaller chunks
    # This is especially useful for long documents that may exceed the token limit
    # or to keep the chunks smaller, so each chunk is more focused

    # In this case, we intentionally set the chunk_size to 1100 tokens, to have the smallest document (document 2) intact
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Split the documents into smaller chunks
    chunked_docs  = text_splitter.split_documents(documents)

    return chunked_docs 

def create_vectordb(embeddings_model, chunked_docs, collection_name):
    # Create the vector database
    vectordb = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings_model,
        collection_name=collection_name,
        persist_directory="./vector_db"
    )
    return vectordb

def process_docs(pdf_storage_path, collection_name, embeddings_model):
    docs = load_documents(pdf_storage_path)
    print(f"Loaded {len(docs)} documents")
    chunked_docs = chunk_documents(docs)
    print(f"Created {len(chunked_docs)} chunks")
    if chunked_docs:
        print(f"Sample chunk: {chunked_docs[0].page_content[:100]}")
    vectordb = create_vectordb(embeddings_model, chunked_docs, collection_name)
    return vectordb

def run_rag(vectordb, llm):
    # Build prompt
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum. Keep the answer as concise as possible. 

    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True, # Make inspection of document possible
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    return qa_chain
    # to use: qa_chain.invoke('What is Top-P sampling?')

@st.cache_resource
def load_vectordb(_embeddings_model, collection_name, persist_dir="./vector_db"):
    """
    Load a specific collection from the vector database.
    """
    try:
        vectordb = Chroma(
            collection_name=collection_name,
            embedding_function=_embeddings_model,
            persist_directory=persist_dir
        )
        st.success(f"✅ Loaded '{collection_name}' with {vectordb._collection.count()} documents")
        return vectordb
    except Exception as e:
        st.error(f"❌ Could not load collection '{collection_name}': {e}")
        return None

# def test_vectordb(vectordb, tests):
#     """Comprehensive vector database test"""
    
#     # 1. Check if vectordb exists
#     if vectordb is None:
#         st.write("❌ Vector database is None!")
#         return
    
#     # 2. Check document count
#     try:
#         count = vectordb._collection.count()
#         st.write(f"✅ Vector database has {count} documents")
#     except Exception as e:
#         print(f"❌ Error getting count: {e}")
#         return
    
#     if count == 0:
#         st.write("❌ No documents in vector database!")
#         return  
    
#     for query in tests:
#         st.write(f"\n{'='*60}")
#         st.write(f"Query: {query}")
#         st.write('='*60)
        
#         try:
#             results = vectordb.similarity_search_with_relevance_scores(query, k=3)
            
#             if not results:
#                 st.write("No results found")
#                 continue
            
#             for i, (doc, score) in enumerate(results):
#                 st.write(f"\nResult {i+1} (Relevance: {score:.4f})")
#                 st.write(f"Content: {doc.page_content[:300]}...")
#                 st.write(f"Metadata: {doc.metadata}")
        
#         except Exception as e:
#             st.write(f"❌ Error during search: {e}")
    
#     st.write("\n✅ Vector database test complete!")

# # ⚠️⚠️⚠️ This is the key step
# # We can set the threshold for the retriever, this is the minimum similarity score for the retrieved documents
# retriever_w_threshold = vectordb.as_retriever(
#         search_type="similarity_score_threshold",
#         # There is no universal threshold, it depends on the use case
#         search_kwargs={'score_threshold': 0.20}
#     )
# # The `llm` is defined earlier in the notebook (using GPT-4o-mini)
# rag_chain = RetrievalQA.from_llm(
#     retriever=retriever_w_threshold, llm=llm
# )

# # Now we can use the RAG pipeline to ask questions
# # Let's ask a question that we know is in the documents
# llm_response = rag_chain.invoke('What is Top-P sampling?')
# print(llm_response['result'])

# # Use the high-level retriever object to retrieve the relevant documents
# retriever_w_threshold.invoke('What is Temperature in LLMs?')

# # Now let's break down and see what are the "splitted_documents" that are used in the RAG pipeline
# # We can do this by using the vectordb object that we have created
# # k=4 is the default value for the number of retrieved documents
# retrieved_documents = vectordb.similarity_search_with_relevance_scores("What is Top-P sampling?", k=4)


# Compared to the rag pipelines that we used above, this cell allows a custom prompt to be used
# This is useful for customizing the prompt to be used in the retrieval QA chain
# The prompt below is the standard template that is used in the retrieval QA chain
# It also includes the "documents" that are used in the prompt