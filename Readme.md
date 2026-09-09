# 📚 PDF Reader Student Assistant - RAG Application

A powerful AI-powered PDF question-answering system built with **Retrieval Augmented Generation (RAG)** technology. Upload any PDF and ask questions about its content - the assistant uses advanced embeddings and LLM inference to provide accurate, context-based answers.

## ✨ Features

- **PDF Upload & Processing**: Upload any PDF file for analysis
- **Text Extraction**: Automatic text extraction using PyMuPDF
- **Semantic Search**: Uses FAISS for fast vector similarity search
- **AI-Powered Answers**: Groq-powered LLM for intelligent response generation
- **Chunk Visualization**: See which parts of the document were used for answers
- **Session State Management**: Process multiple documents in one session
- **Beautiful UI**: Modern, intuitive Streamlit interface

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Streamlit 1.28.1 | Web interface & interaction |
| PDF Processing | PyMuPDF 1.23.8 | PDF text extraction |
| Embeddings | Sentence Transformers 2.2.2 | Text vectorization (all-MiniLM-L6-v2) |
| Vector Search | FAISS 1.7.4 | Fast similarity search |
| LLM | Groq API (Mixtral-8x7b) | Answer generation |
| Numerical | NumPy 1.24.3, SciPy 1.11.2 | Matrix operations |
| ML Framework | PyTorch 2.0.1 | Deep learning backend |

## 📋 Requirements

### System Requirements
- Python 3.10 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB disk space for models

### Groq API
- Free account at https://console.groq.com
- API key (generate in your account settings)

## 🚀 Deployment to Streamlit Cloud

### Step 1: Prepare Your GitHub Repository

1. **Create a GitHub Account** (if you don't have one):
   - Visit https://github.com/signup
   - Sign up with your email
   - Verify your email

2. **Create a New Repository**:
   - Click the "+" icon → "New repository"
   - Repository name: `pdf-assistant-rag` (or any name)
   - Add description: "AI-powered PDF Q&A with RAG"
   - Select "Public"
   - Check "Add a README file"
   - Click "Create repository"

### Step 2: Upload Files to GitHub (No Terminal/VSCode Required)

1. **Navigate to Your Repository**:
   - Go to your newly created repository URL

2. **Add Files Using GitHub Web Interface**:
   - Click "Add file" button
   - Select "Create new file" or "Upload files"

   **Method A - Create files directly in GitHub**:
   - Click "Create new file"
   - Name: `app.py`
   - Paste the app.py code from this package
   - Click "Commit changes"
   - Repeat for `requirements.txt`, `.gitignore`, and `README.md`

   **Method B - Upload files directly**:
   - Click "Add file" → "Upload files"
   - Drag and drop all files (app.py, requirements.txt, .gitignore)
   - Click "Commit changes"

3. **Verify Files Are Present**:
   - Your repository should contain:
     ```
     ├── app.py
     ├── requirements.txt
     ├── .gitignore
     └── README.md
     ```

### Step 3: Deploy to Streamlit Cloud

1. **Sign Up for Streamlit Cloud**:
   - Visit https://streamlit.io/cloud
   - Click "Sign in with GitHub"
   - Authorize Streamlit to access your GitHub account
   - Accept the terms

2. **Deploy Your Application**:
   - Click "Create app"
   - Select your repository: `pdf-assistant-rag`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets (API Key)**:
   - Wait for initial deployment to complete (may take 2-3 minutes)
   - Click the three-dot menu (⋯) in the top right
   - Select "Settings"
   - Go to "Secrets" tab
   - Add your Groq API key (you'll paste this in the app UI instead)
   - Or leave blank - users will enter it in the sidebar

### Step 4: Test Your Deployment

1. **Access Your App**:
   - Your app URL will be: `https://[your-username]-pdf-assistant-rag.streamlit.app`
   - Share this link with anyone to use your assistant

2. **First Run**:
   - Navigate to your app URL
   - Go to "Upload & Process" tab
   - Upload a sample PDF
   - Wait for processing
   - Get your Groq API key from https://console.groq.com/keys
   - Paste it in the sidebar
   - Ask a question!

## 📖 How It Works

### Architecture

```
User Input (PDF) 
    ↓
[PyMuPDF] Extract Text
    ↓
[Text Splitter] Create Chunks (500 chars, 50 overlap)
    ↓
[Sentence Transformer] Generate Embeddings
    ↓
[FAISS] Build Vector Index
    ↓
User Question
    ↓
[Vector Search] Retrieve Top 5 Chunks
    ↓
[Groq API] Generate Answer with Context
    ↓
Display Answer + Source Chunks
```

### RAG Pipeline Explained

1. **Document Processing**: PDF is converted to text and split into manageable chunks
2. **Embedding Generation**: Each chunk is converted to a numerical vector (768 dimensions)
3. **Index Creation**: Vectors are indexed in FAISS for fast retrieval
4. **Query Processing**: User's question is embedded using the same model
5. **Retrieval**: Top 5 most similar chunks are retrieved using vector similarity
6. **Generation**: Retrieved chunks are sent as context to Groq LLM
7. **Response**: AI generates an answer grounded in the document context

## 🔑 Getting Your Groq API Key

1. Visit https://console.groq.com
2. Sign up with your email or Google/GitHub account
3. Click "API Keys" in the left sidebar
4. Click "Create API Key"
5. Copy the key (it starts with `gsk_`)
6. Paste it in the sidebar when using the app

**Note**: Free tier includes 14,400 tokens per minute - more than enough for student use.

## 🎯 Example Queries

Once you've uploaded a PDF, try these types of questions:

- **Summary**: "Summarize chapter 3"
- **Definition**: "What is machine learning?"
- **Comparison**: "Compare the two approaches discussed"
- **Details**: "Explain the methodology used in the study"
- **Analysis**: "What are the limitations mentioned?"
- **Timeline**: "What happened in 2020 according to this document?"

## ⚙️ Configuration

### Temperature Setting
- **0.0-0.3**: More factual, precise answers (recommended for technical docs)
- **0.3-0.7**: Balanced responses
- **0.7-1.0**: More creative, varied responses

### Chunk Size
- Default: 500 characters with 50-character overlap
- Larger chunks = more context but slower processing
- Smaller chunks = faster but may lose context

## 🐛 Troubleshooting

### "Error loading embedding model"
- **Cause**: Internet connection issue or model download failure
- **Solution**: Refresh the page; Streamlit will retry

### "API key error"
- **Cause**: Invalid Groq API key
- **Solution**: Verify key from https://console.groq.com/keys

### "FAISS index error"
- **Cause**: PDF has very little text
- **Solution**: Ensure PDF contains at least 500 characters of text

### App is slow on first load
- **Cause**: First time downloading embedding model (~100MB)
- **Solution**: Normal on first run; subsequent loads are instant (cached)

### "No relevant content found"
- **Cause**: Question doesn't match document content
- **Solution**: Try rephrasing the question or asking about different content

## 📊 Model Details

### Embedding Model: all-MiniLM-L6-v2
- **Dimensions**: 384
- **Size**: ~22 MB
- **Speed**: Fast (suitable for real-time)
- **Accuracy**: Excellent for semantic search

### LLM: Mixtral-8x7b (via Groq)
- **Type**: Mixture of Experts model
- **Tokens**: Supports up to 32k token context
- **Speed**: Extremely fast inference via Groq
- **Multilingual**: Supports 40+ languages

## 🔒 Privacy & Security

- PDFs are processed locally (text extraction on Streamlit servers)
- Embeddings are generated on Streamlit servers
- Only questions and context are sent to Groq API
- API key is stored in browser session (not saved)
- No PDFs are logged or stored permanently

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Groq API Documentation](https://console.groq.com/docs)
- [Sentence Transformers](https://www.sbert.net)
- [RAG Explained](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] All files uploaded (app.py, requirements.txt, .gitignore, README.md)
- [ ] Streamlit Cloud account created
- [ ] App deployed and accessible
- [ ] Groq API key obtained
- [ ] Tested with sample PDF
- [ ] Share link with friends/classmates!

## 🆘 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Streamlit Cloud documentation
3. Check Groq API status at https://status.groq.com

---

**Happy learning! 🎓**
