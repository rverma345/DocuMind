# 🧠 DocuMind: Universal Document Intelligence Chatbot

DocuMind is an **AI-powered assistant** that can intelligently answer questions from your **uploaded documents** (PDFs) and perform **web searches** when required.  
It combines **LangChain, OpenAI, ChromaDB, and Streamlit** to deliver context-aware, source-backed responses.

---

## ✨ Features

- 📂 **Document Ingestion** – Upload multiple PDFs, split into chunks, and store embeddings in **ChromaDB**.  
- 🔍 **Smart Query Routing** – Decides whether to answer using:
  - **Document Search** (if high document relevance).  
  - **Web Search** (if query is external or recent).  
  - **Hybrid Search** (mix of both).  
- 🤖 **LLM-Powered Answers** – Uses OpenAI’s GPT model to generate clear, concise answers.  
- 📌 **Source Attribution** – Always provides references from documents or web links.  
- 💬 **Chat History** – Maintains conversation context within the Streamlit app.  

---

## 🚀 Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework  
- [LangChain](https://www.langchain.com/) – Orchestration  
- [OpenAI](https://openai.com/) – LLM + Embeddings  
- [ChromaDB](https://www.trychroma.com/) – Vector database for document search  
- [Serper API](https://serper.dev/) – Google Search API  

---

## 📂 Project Structure

```
.
├── app.py              # Main Streamlit app
├── ingestion.py        # PDF ingestion, chunking & embedding
├── search.py           # Document/Web/Hybrid search logic
├── route.py            # Query router
├── llm_results.py      # LLM response generator
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignore secrets & large files
└── vector_store/       # Local ChromaDB (ignored in git)
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/DocuMind.git
cd DocuMind
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables  
Create a `.env` file in the root folder:
```ini
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

⚠️ Never commit `.env` to GitHub.  

---

## ▶️ Run the App
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.  

---

## 🧪 Usage

1. Upload your PDFs from the sidebar.  
2. Click **Process** to embed them into ChromaDB.  
3. Ask questions in the chat box:  
   - *“Summarize the second chapter from my notes.”*  
   - *“What are the latest AI trends in 2025?”* (routes to web search).  
   - *“Compare CNN and RNN from my uploaded material.”*  

---

## 🛡️ Security

- API keys are stored in `.env`.  
- Uploaded PDFs and vector DB are ignored in Git.  
- Safe fallback: If no relevant context → model replies *“I don’t know.”*  

