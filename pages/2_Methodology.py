import streamlit as st

st.title("Methodology")

mermaid_chart = """
```mermaid
graph TB
    Start([🚀 User Opens Application]) --> Auth{🔐 Password<br/>Protection}
    Auth -->|Incorrect| AuthFail[❌ Access Denied]
    Auth -->|Correct| SelectUseCase[📋 Select Use Case]
    
    SelectUseCase --> Choice{Which Service?}
    
    Choice -->|Option 1| License[🎫 License Finder]
    Choice -->|Option 2| Company[🏢 Company Setup Guide]
    Choice -->|Option 3| Form[📄 Form Checker]
    
    subgraph PreProcessing["🔧 Pre-Processing Done Once"]
        P1[Download PDFs] --> P2[Load PDFs]
        P2 --> P3[Chunk Text<br/>Size: 1500 chars<br/>Overlap: 100 chars]
        P3 --> P4[Generate Embeddings<br/>Azure OpenAI]
        P4 --> P5[(Chroma Vector DB<br/>Collection: licenses<br/>Collection: localcompany)]
    end
    
    License --> L1[Load Vector DB:<br/>licenses]
    Company --> C1[Load Vector DB:<br/>localcompany_setup]
    
    L1 --> L2[💭 User Enters Question]
    C1 --> C2[💭 User Enters Question]
    
    L2 --> L3[Embed Query]
    C2 --> C3[Embed Query]
    
    L3 --> L4[Similarity Search<br/>k=4 documents]
    C3 --> C4[Similarity Search<br/>k=4 documents]
    
    L4 --> L5[Build Prompt:<br/>Context + Question]
    C4 --> C5[Build Prompt:<br/>Context + Question]
    
    L5 --> L6[🤖 Azure OpenAI<br/>GPT-4]
    C5 --> C6[🤖 Azure OpenAI<br/>GPT-4]
    
    L6 --> L7[📤 Answer + Sources]
    C6 --> C7[📤 Answer + Sources]
    
    Form --> F1[📤 Upload Form<br/>PDF/Image/ZIP]
    F1 --> F2[🖼️ Convert to Images<br/>Base64 Encode]
    F2 --> F3[👁️ Azure OpenAI<br/>Vision Model]
    F3 --> F4[🔍 Validate Form<br/>Check Completeness]
    F4 --> F5[📊 Generate Report<br/>Issues + Recommendations]
    
    L7 --> End([✅ End])
    C7 --> End
    F5 --> End
    
    AuthFail --> EndFail([❌ End])
    
    P5 -.->|Persistent Storage| L1
    P5 -.->|Persistent Storage| C1
    
    style Start fill:#90EE90
    style End fill:#90EE90
    style EndFail fill:#FFB6C1
    style PreProcessing fill:#E6F3FF,stroke:#333,stroke-width:2px
    style P5 fill:#87CEEB
    style L6 fill:#FFE6CC
    style C6 fill:#FFE6CC
    style F3 fill:#FFE6CC
```
"""

st.markdown(mermaid_chart)