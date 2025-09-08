from route import query_router
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import requests, os
from dotenv import load_dotenv
from llm_results import generate_result

load_dotenv()


# 1. Load Chroma Vector Store

def load_vector_store(persist_dir="vector_store"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings)



# 2. Document Search

def document_search(query, vector_store, top_k=3):
    results = vector_store.similarity_search_with_score(query, k=top_k)
    normalized_results = [(doc, 1 / (1 + score)) for doc, score in results]
    return normalized_results



# 3. Web Search

def web_search(query, num_results=3):
    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": num_results}
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()



# 4. Hybrid Search

def hybrid_search(query, vector_store, top_k=3, num_results=3):
    doc_results = document_search(query, vector_store, top_k=top_k)
    web_results = web_search(query, num_results=num_results)

    docs = [
        {"source": "document", "content": doc.page_content, "score": score}
        for doc, score in doc_results
    ]

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



# 5. Search + Route + LLM

def searching_and_produce_output(query, vector_store, top_k=3, num_results=3):
    results = document_search(query, vector_store, top_k=top_k) if vector_store else []
    best_doc, best_score = (results[0] if results else (None, 0.0))

    mode = query_router(query, best_score)

    context = ""
    if mode == "document_search":
        context = "\n\n".join([doc.page_content for doc, _ in results])
    elif mode == "web_search":
        web_res = web_search(query, num_results=num_results)
        context = "\n\n".join(
            [f"{item.get('title')}: {item.get('snippet')} ({item.get('link')})"
             for item in web_res.get("organic", [])]
        )
    elif mode == "hybrid_search":
        hybrid_res = hybrid_search(query, vector_store, top_k=top_k, num_results=num_results)
        doc_text = "\n\n".join([doc["content"] for doc in hybrid_res["documents"]])
        web_text = "\n\n".join([f"{item['title']}: {item['snippet']} ({item['link']})"
                                for item in hybrid_res["web"]])
        context = doc_text + "\n\n" + web_text
    else:
        context = "No context available."

    return generate_result(query=query, context=context)
