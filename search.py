from route import query_router
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import requests, os
from dotenv import load_dotenv

load_dotenv()

# --------------------------
# 1. Load Chroma Vector Store
# --------------------------
def load_vector_store(persist_dir="vector_store"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
    return vector_store

# --------------------------
# 2. Document Search
# --------------------------
def document_search(query, vector_store, top_k=3):
    results = vector_store.similarity_search_with_score(query, k=top_k)
    normalized_results = [(doc, 1 / (1 + score)) for doc, score in results]
    return normalized_results

# --------------------------
# 3. Web Search
# --------------------------
def web_search(query, num_results=3):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": num_results}
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# --------------------------
# 4. Hybrid Search
# --------------------------
def hybrid_search(query, vector_store, top_k=3, num_results=3):
    doc_results = document_search(query, vector_store, top_k=top_k)
    web_results = web_search(query, num_results=num_results)

    # Documents
    docs = [
        {"source": "document", "content": doc.page_content, "score": score}
        for doc, score in doc_results
    ]

    # Web results
    web_items = []
    if "organic" in web_results:
        web_items = [
            {
                "source": "web",
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            }
            for item in web_results["organic"]
        ]

    return {"documents": docs, "web": web_items}


def search(query,vector_store,top_k=3,num_results=3):

    results=document_search(query,vector_store),top_k=top_k)
    if results:  # If we got any doc results
        best_doc, best_score = results[0]
    else:
        # No docs available → force web
        best_doc, best_score = (None, 0.0)

    #routing
    mode= query_router(query,best_score)

    if mode=='document_search':
        document_search