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

# Page config
st.set_page_config(
    page_title="Venturely",
    page_icon="💡",
    layout="centered"
)

# App title
st.title("💡 Venturely")
st.markdown("""
Welcome to **Venturely**, your personal guide to starting a business in Singapore!  

We combine **LLMs with official government documents** to give you **step-by-step guidance** on business registration and licensing. Whether you’re figuring out the licenses you need or the steps to set up a company, Venturely makes the process **simpler, faster, and more approachable**.  

### What You Can Do Here:
- **License Finder**: Discover exactly which licenses your business needs based on your niche.  
- **How-to Set Up a Local Company**: Get a clear, step-by-step roadmap for registering your company, backed by official ACRA guides.  

Let’s make starting your business less stressful and more enjoyable! 🚀
""")

# Load models
embeddings_model = rag.load_emb_model()
llm = rag.load_llm()

# Select which topic
st.markdown("### Select use case:")

# Hide the default label by passing an empty string
collection_choice = st.selectbox(
    "",  # empty label
    ["License Finder", "How-to Set Up a Local Company"]
)

# # Change color of a box or header based on selection
# if collection_choice == "License Finder":
#     st.markdown('<div style="background-color:#D0F0C0; padding:10px; border-radius:5px">'
#                 '<b>License Finder selected</b></div>', unsafe_allow_html=True)
# else:
#     st.markdown('<div style="background-color:#ADD8E6; padding:10px; border-radius:5px">'
#                 '<b>How-to Set Up a Local Company selected</b></div>', unsafe_allow_html=True)

# Map to collection names
collection_map = {
    "License Finder": "licenses",
    "How-to Set Up a Local Company": "localcompany_setup"
}

collection_name = collection_map[collection_choice]

# Load the selected collection
vectordb = rag.load_vectordb(embeddings_model, collection_name)

# Only show query interface if vectordb loaded successfully
if vectordb is not None:
    # user_query = st.text_input(f"Ask about {collection_choice.lower()}:")
    if collection_choice == "License Finder":
        st.markdown('''
            <div style="background-color:#D0F0C0; padding:10px; border-radius:5px">
                <h3 style="margin:0;">Ask about License Finder</h3>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="background-color:#ADD8E6; padding:10px; border-radius:5px">
                <h3 style="margin:0;">Ask about How-to Set Up a Local Company</h3>
            </div>
        ''', unsafe_allow_html=True)
    
    user_query = st.text_input("")
    
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
















