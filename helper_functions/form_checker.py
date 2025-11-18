import streamlit as st
from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from helper_functions import constants, prompts
import PyPDF2
import io

# ... (keep your existing load_llm, load_emb_model, get_template, run_rag, load_vectordb functions)

def extract_pdf_text(uploaded_file):
    """Extract text content from uploaded PDF."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def check_form(llm, form_content):
    """Check form using LLM with form validation prompt."""
    try:
        # Use LLM directly (no RAG)
        response = llm.invoke(prompts.form_checker_prompt_template)
        return response.content
    except Exception as e:
        st.error(f"Error checking form: {str(e)}")
        return None