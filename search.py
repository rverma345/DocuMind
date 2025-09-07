from route import query_router
from langchain_community.vectorstores import Chroma
import requests
from dotenv import load_dotenv
import requests,os


load_dotenv()


def document_search(query,vector_store,top_k=3):
    results=vector_store.similarity_search_with_score(query,k=top_k)
    return results


def web_search(query, num_results=3):
    url = "https://google.serper.dev/search"

    payload = {"q": query, "num": num_results}
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),  # load from .env
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def hybrid_search(query, vector_store, top_k=3, num_results=3):
    """
    Combines document search + web search
    """
    doc_results = document_search(query, vector_store, top_k=top_k)
    web_results = web_search(query, num_results=num_results)

    # Extract docs in a clean format
    docs = [{"source": "document", "content": doc.page_content, "score": score} 
            for doc, score in doc_results]

    # Extract web search in a clean format
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


def searching(query):
    score