# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions import llm, rag
# from logics.customer_query_handler import process_user_message


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")

# Only run when button is clicked
if st.button("Process Documents"):
    emb_model = rag.load_emb_model()
    with st.spinner("Processing documents..."):
        # file_path = "./data/license_sample"
        file_path = "./data/license_full"
        
        # Process documents
        vectordb = rag.process_docs(file_path, "licenses", emb_model)
        
        # Store in session state so it persists
        st.session_state.vectordb = vectordb
        
        st.success("Documents processed!")

# Test vectordb if it exists
if 'vectordb' in st.session_state:
    llm = rag.load_llm()
    # test_str = "What license should i apply to be a taxi driver?"
    test_str = "Which licenses should i apply to be a cafe owner?"
    st.write(rag.run_rag(vectordb, llm).invoke(test_str))
    
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
