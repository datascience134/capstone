# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions import llm, rag
# from logics.customer_query_handler import process_user_message


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

# Load embeddings model
embeddings_model = rag.load_emb_model()
llm = rag.load_llm()

# Select which collection to query
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
                qa_chain = rag.run_rag(vectordb, llm)
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







# # Only run when button is clicked
# if st.button("License Finder"):
#     st.markdown('''Find the licenses that you need to apply for based on your dream business''')
#     emb_model = rag.load_emb_model()
#     llm = rag.load_llm()
#     with st.spinner("Processing..."):
#         # file_path = "./data/license_sample"
#         file_path = "./data/licenses_full"
        
#         # Process documents
#         vectordb = rag.process_docs(file_path, "licenses", emb_model)
        
#         # Store in session state so it persists
#         st.session_state.vectordb = vectordb
        
#         st.success("RAG is ready")

#     if 'vectordb' in st.session_state:
    
#         form = st.form(key="form")
#         form.subheader("Prompt")

#         user_prompt = form.text_area("Enter your prompt here", height=200)
#         # submit button inside the form
#         submitted = form.form_submit_button("Submit")

#         if submitted:
    
#             st.toast(f"User Input Submitted - {user_prompt}")

#             st.divider()
#             response = rag.run_rag(vectordb, llm).invoke(user_prompt)
#             st.write(response['result'])
















# Test vectordb if it exists
# if 'vectordb' in st.session_state:
#     llm = rag.load_llm()
#     # test_str = "What license should i apply to be a taxi driver?"
#     test_str = "Which licenses should i apply to be a cafe owner?"
#     st.write(rag.run_rag(vectordb, llm).invoke(test_str))
    
    # st.subheader("Test Vector Database")
    
    # test_queries = [
    #     "What license should i apply to be a taxi driver?",
    # ]
    
    # if st.button("Run Tests"):
    #     rag.test_vectordb(st.session_state.vectordb, test_queries)

# form = st.form(key="form")
# form.subheader("Prompt")

# user_prompt = form.text_area("Enter your prompt here", height=200)
# # submit button inside the form
# submitted = form.form_submit_button("Submit")

# if submitted:
    
#     st.toast(f"User Input Submitted - {user_prompt}")

#     st.divider()
#     # st.write(llm.get_embedding(user_prompt))
#     # st.write(llm.get_completion(user_prompt))
#     st.write(run_rag(vectordb, llm).invoke(user_prompt))

#     # response, course_details = process_user_message(user_prompt)
#     # st.write(response)

#     st.divider()

    # print(course_details)
    # df = pd.DataFrame(course_details)
    # df 
