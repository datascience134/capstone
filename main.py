# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions import rag


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
    ["Licenses", "Local Company Setup"]
)

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
















