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
        # Build prompt directly
        prompt = f'''
        You are a Form Validation Assistant. Your job is to review a submitted form
            for correctness, completeness, and consistency.

            Check for:
            1. Missing or blank required fields.
            2. Incomplete fields (partially filled, unclear, or placeholder text left in).
            3. Incorrect information:
            - Wrong or invalid NRIC (invalid checksum, wrong structure)
            - Invalid or incomplete addresses
            - Incorrect postal codes
            - Wrong phone numbers or email formats
            - Incorrect dates or inconsistent formats
            4. Logical inconsistencies:
            - Dates that contradict each other
            - Age inconsistent with date of birth
            - Names or IDs not matching across sections
            - Conflicting answers in different parts of the form
            5. Signature issues:
            - Missing signatures
            - Signature mismatch (if multiple signatures are present)
            6. Document issues:
            - Missing supporting documents that the form requires
            7. Formatting issues:
            - Wrong date formats
            - Incorrect checkboxes
            - Unclear handwriting (from scanned PDFs)

            Provide your response in this structure:
            1. Summary
            2. Issues Found (detailed)
            3. Recommendations for Correction

            Here is the form content to validate:

            ---
            {form_content}
            ---

            Please provide your validation report:
        '''

        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        st.error(f"Error checking form: {str(e)}")
        return None