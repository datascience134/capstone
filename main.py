# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions import llm, rag, form_checker


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    
    return False


if not check_password():
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Venturely"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Venturely")

st.markdown('''
    This is an LLM app that will guide new entrepreneurs to register and start a business in Singapore. It consolidates official government information to provide personalized guidance on business registration and licensing. This helps to make the starting process of a business easier and more approachable.  
            
    ''')

# Load models
embeddings_model = rag.load_emb_model()
llm = rag.load_llm()

# Select which topic
collection_choice = st.selectbox(
    "Select topic:",
    ["Licenses", "Local Company Setup", "Form Checker"]
)

# Handle different topics
if collection_choice == "Form Checker":
    st.subheader("📋 Form Validation")
    st.write("Upload a form (PDF) to check for errors and completeness.")
    
    uploaded_file = st.file_uploader("Upload Form (PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        if st.button("Check Form"):
            with st.spinner("Analyzing form..."):
                # Extract text from PDF
                form_content = form_checker.extract_pdf_text(uploaded_file)
                
                if form_content:
                    st.write(f"📄 Extracted {len(form_content)} characters from form")
                    
                    # Check form using LLM
                    result = form_checker.check_form(llm, form_content)
                    
                    if result:
                        st.write("**Validation Report:**")
                        st.write(result)
                        
                        # Optional: Show extracted text in expander
                        with st.expander("View Extracted Form Content"):
                            st.text(form_content[:2000])  # Show first 2000 chars
                else:
                    st.error("Could not extract text from PDF")

else:
    # RAG-based topics (Licenses and Local Company Setup)
    
    # Map to collection names
    collection_map = {
        "Licenses": "licenses",
        "Local Company Setup": "localcompany_setup"
    }
    
    collection_name = collection_map[collection_choice]
    
    # Load the selected collection
    vectordb = rag.load_vectordb(embeddings_model, collection_name)
    
    # Only show query interface if vectordb loaded successfully
    if vectordb is not None:
        user_query = st.text_input(f"Ask about {collection_choice.lower()}:")
        
        if user_query:
            with st.spinner("Searching..."):
                try:
                    qa_chain = rag.run_rag(vectordb, llm, collection_name)
                    result = qa_chain.invoke(user_query)
                    
                    st.write("**Answer:**")
                    st.write(result['result'])
                    
                    with st.expander("Source Documents"):
                        for i, doc in enumerate(result['source_documents']):
                            st.write(f"**Source {i+1}:**")
                            st.write(doc.page_content[:300])
                            
                except Exception as e:
                    st.error(f"Error during query: {str(e)}")
    else:
        st.warning("Vector database not loaded. Please check the logs above.")



















