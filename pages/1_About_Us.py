import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

# Main container
st.title("💡 About Venturely")

st.markdown("""
**Venturely** is a smart LLM-powered app designed to guide new entrepreneurs in Singapore through the process of registering and starting a business. 
We consolidate official government information into a personalized, conversational experience, making business registration simpler, clearer, and approachable.
""")

st.subheader("🚀 Our Mission")
st.markdown("""
Starting a business can be overwhelming. Entrepreneurs often struggle to find and understand all the necessary steps, licenses, and formal requirements for their specific business type. 
This can deter potential founders and create extra administrative workload for government agencies.

**Venturely simplifies this process** by providing tailored guidance based on official documents, helping users confidently navigate the steps needed to launch their business.
""")

st.subheader("✨ Key Features")
st.markdown("""
**1. License Finder**  
- Uses **Retrieval-Augmented Generation (RAG)** to identify which licenses you need based on your unique business niche.  
- Pulls from PDFs of official licenses from [GoBusiness Singapore](https://licensing.gobusiness.gov.sg/licence-directory).  
- Makes sense of 31 pages of dense, formal license information so users can understand their requirements quickly, e.g., setting up a home café.  

**2. How-to Set Up a Local Company**  
- Guides users **step-by-step** in registering a company in Singapore.  
- Uses RAG on PDFs from [ACRA](https://www.acra.gov.sg/how-to-guides/setting-up-a-local-company) to explain all 13 steps and their caveats in clear, conversational language.  
- Reduces mistakes, stress, and delays while keeping guidance accurate and document-backed.
""")

st.subheader("📊 Our Approach")
st.markdown("""
Venturely combines **LLMs with official government data** to deliver personalized, actionable guidance.  
We transform formal documents into an approachable, conversational experience that helps entrepreneurs:  
- Understand requirements quickly  
- Avoid mistakes in applications  
- Navigate complex processes confidently  

By bridging the gap between official resources and user needs, Venturely empowers Singapore’s entrepreneurs to start their businesses efficiently and correctly.
""")


with st.expander("Disclaimer"):
    st.write('''
             IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. 
             The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters. 
             Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
             You assume full responsibility for how you use any generated output.
             Always consult with qualified professionals for accurate and personalized advice.
             ''')

# Add a footer
st.markdown("---")
st.markdown("© 2025 Venturely. All rights reserved.")