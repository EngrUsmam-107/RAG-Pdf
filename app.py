import streamlit as st
import pymupdf
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="PDF Reader Student Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📚 PDF Reader Student Assistant")
st.markdown("### AI-Powered Document Q&A with Retrieval Augmented Generation")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password", key="groq_key")
    
    st.markdown("---")
    st.subheader("📖 How It Works")
    st.info("""
    1. Upload a PDF file
    2. The app extracts text and creates embeddings
    3. Ask questions about the content
    4. Get AI-generated answers based on document context
    
    **Tech Stack:**
    - Sentence Transformers for embeddings
    - FAISS for vector similarity search
    - Groq for fast LLM inference
    """)
    
    st.markdown("---")
    st.markdown("**Temperature:** Controls response creativity (0=factual, 1=creative)")
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)


# Initialize session state
if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None
if "embeddings_index" not in st.session_state:
    st.session_state.embeddings_index = None
if "text_chunks" not in st.session_state:
    st.session_state.text_chunks = None
if "model" not in st.session_state:
    st.session_state.model = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None


@st.cache_resource
def load_embedding_model():
    """Load sentence transformer model (cached for efficiency)"""
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model
    except Exception as e:
        st.error(f"Error loading embedding model: {str(e)}")
        return None


def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF using PyMuPDF"""
    try:
        pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        metadata = {
            "pages": len(pdf_document),
            "title": pdf_document.metadata.get("title", "Unknown")
        }
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.get_text()
        
        pdf_document.close()
        return text, metadata
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None, None


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    
    return [chunk for chunk in chunks if len(chunk) > 50]


def create_faiss_index(chunks, model):
    """Create FAISS index from text chunks"""
    try:
        embeddings = model.encode(chunks, convert_to_numpy=True)
        embeddings = embeddings.astype(np.float32)
        
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        return index
    except Exception as e:
        st.error(f"Error creating FAISS index: {str(e)}")
        return None


def retrieve_relevant_chunks(query, model, index, chunks, k=5):
    """Retrieve top-k relevant chunks for the query"""
    try:
        query_embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
        distances, indices = index.search(query_embedding, k)
        
        relevant_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
        return relevant_chunks
    except Exception as e:
        st.error(f"Error retrieving chunks: {str(e)}")
        return []


def generate_answer(question, context, api_key, temperature):
    """Generate answer using Groq API"""
    try:
        client = Groq(api_key=api_key)
        
        system_prompt = """You are a helpful student assistant. Answer questions based on the provided document context. 
        If the answer is not in the context, say "I cannot find this information in the provided document."
        Be clear, concise, and educational in your responses."""
        
        user_message = f"""Context from document:
{context}

Question: {question}

Please provide a clear and accurate answer based on the context above."""
        
        message = client.messages.create(
            model="mixtral-8x7b-32768",
            max_tokens=1024,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        st.error(f"Error generating answer: {str(e)}")
        return None


# Main application layout
tab1, tab2 = st.tabs(["📤 Upload & Process", "❓ Ask Questions"])

with tab1:
    st.subheader("Upload Your PDF Document")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file is not None:
        if st.button("🔄 Process PDF", use_container_width=True, type="primary"):
            with st.spinner("Processing PDF... This may take a moment"):
                # Extract text
                text, metadata = extract_text_from_pdf(uploaded_file)
                
                if text:
                    st.success(f"✅ PDF processed successfully!")
                    
                    # Display metadata
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Pages", metadata["pages"])
                    with col2:
                        st.metric("Characters", f"{len(text):,}")
                    
                    # Load model and create index
                    st.info("Loading embedding model and creating search index...")
                    model = load_embedding_model()
                    
                    if model:
                        chunks = chunk_text(text)
                        st.write(f"Created {len(chunks)} text chunks")
                        
                        index = create_faiss_index(chunks, model)
                        
                        if index:
                            # Store in session state
                            st.session_state.pdf_data = text
                            st.session_state.embeddings_index = index
                            st.session_state.text_chunks = chunks
                            st.session_state.model = model
                            st.session_state.pdf_name = uploaded_file.name
                            
                            st.success("✅ PDF is ready for questions! Go to the 'Ask Questions' tab.")
                            
                            # Preview
                            with st.expander("📄 Preview First 500 characters"):
                                st.text(text[:500] + "...")

with tab2:
    if st.session_state.pdf_data is None:
        st.warning("⚠️ Please upload and process a PDF first in the 'Upload & Process' tab.")
    else:
        st.subheader(f"Asking questions about: {st.session_state.pdf_name}")
        
        # Display document info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Document", st.session_state.pdf_name.split('.')[0][:20])
        with col2:
            st.metric("Total Chunks", len(st.session_state.text_chunks))
        with col3:
            st.metric("Model", "all-MiniLM-L6-v2")
        
        st.markdown("---")
        
        # Question input
        question = st.text_area(
            "Ask a question about your document:",
            placeholder="e.g., What are the main topics covered? Or: Explain chapter 3 in detail.",
            height=100
        )
        
        if st.button("🔍 Get Answer", use_container_width=True, type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your Groq API key in the sidebar.")
            elif not question.strip():
                st.error("⚠️ Please enter a question.")
            else:
                with st.spinner("Retrieving relevant content and generating answer..."):
                    # Retrieve relevant chunks
                    relevant_chunks = retrieve_relevant_chunks(
                        question,
                        st.session_state.model,
                        st.session_state.embeddings_index,
                        st.session_state.text_chunks,
                        k=5
                    )
                    
                    if relevant_chunks:
                        context = "\n\n".join(relevant_chunks)
                        
                        # Generate answer
                        answer = generate_answer(question, context, api_key, temperature)
                        
                        if answer:
                            st.success("✅ Answer generated successfully!")
                            
                            # Display answer
                            st.markdown("### Answer")
                            st.write(answer)
                            
                            # Display source information
                            with st.expander("📚 Source Chunks Used"):
                                for i, chunk in enumerate(relevant_chunks, 1):
                                    st.markdown(f"**Chunk {i}:**")
                                    st.text(chunk[:300] + "..." if len(chunk) > 300 else chunk)
                                    st.divider()
                    else:
                        st.error("No relevant content found for your question.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<small>PDF Reader Student Assistant | Built with Streamlit, FAISS, and Groq | 2024</small>
</div>
""", unsafe_allow_html=True)
