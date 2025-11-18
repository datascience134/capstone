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
    Cached to prevent reopening connections.
    """
    try:
        # Create vectordb - this will be cached and reused
        vectordb = Chroma(
            collection_name=collection_name,
            embedding_function=_embeddings_model,
            persist_directory=persist_dir
        )
        return vectordb
    except Exception as e:
        st.error(f"❌ Could not load collection '{collection_name}': {str(e)}")
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