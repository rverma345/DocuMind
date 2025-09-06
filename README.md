# 📚 Universal Knowledge Assistant Chatbot  

A Retrieval-Augmented Generation (**RAG**) application that answers user queries using:  
- **Uploaded documents (PDFs)**  
- **Web search (Serper API)**  
- **Or a combination of both**  

Built with **LangChain + OpenAI + Streamlit**, designed for research teams, legal firms, and businesses.  

---

## 🚀 Features
- 📂 Upload multiple PDFs → semantic search with vector DB  
- 🌐 Auto-switch to web search when docs lack info  
- 🧠 Hybrid answers combining docs + web results  
- 📝 Citations (filename + page numbers)  
- 💬 Interactive chat UI (Streamlit)  

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**  
   Copy `.env.example` → `.env` and fill in your keys:
   ```bash
   OPENAI_API_KEY=your_openai_key
   SERPER_API_KEY=your_serper_key
   VECTOR_DB_PATH=./vector_store
   ```

---

## ▶️ Usage

### 1. Ingest Documents
```bash
python ingestion.py
```

### 2. Run the Chatbot
```bash
streamlit run app.py
```

Upload PDFs in the app and start chatting!

---

## 📂 Project Structure
```
.
├── app.py              # Streamlit app (chat interface)
├── ingestion.py        # PDF loading + indexing
├── retrieval.py        # Vector DB retrieval
├── router.py           # Query routing (docs/web/hybrid)
├── utils.py            # Helper functions
├── config.py           # Loads env variables
├── requirements.txt
├── README.md
├── .env.example
├── data/               # PDF storage (ignored in git)
└── vector_store/       # Persisted embeddings (ignored in git)
```

---

## 🔒 Notes
- Do **not** push your `.env` file (already in `.gitignore`).  
- For collaborators, share only `.env.example`.  
- If uploading sensitive PDFs, keep `data/` folder ignored in git (already handled).  
