import streamlit as st
from helper_functions import prompts
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
        prompt = prompts.form_checker_prompt_template.format(
            context=form_content
        )
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        st.error(f"Error checking form: {str(e)}")
        return None