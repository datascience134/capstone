import streamlit as st
from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

from helper_functions import prompts, constants


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

def get_template(collection_name):
    """Get the appropriate template based on collection."""
    
    templates = {
        "licenses": prompts.license_finder_prompt_template,
        "localcompany_setup": prompts.localcompany_setup_prompt_template,
    }
    
    return templates.get(collection_name, templates["licenses"])

def run_rag(vectordb, llm, collection_name):
    # Get appropriate template
    template = get_template(collection_name)
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
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
