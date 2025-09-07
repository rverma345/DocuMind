def query_router(query: str,doc_score: float):
    
    web_search_keywords=[
            "latest", "current", "2024", "2025", "trend", "price", "stock",
            'compare','alternatives to','vs','versus',
            'trends', 'price', 'stock'
            'explain','how does','what is the'
    ]
    query_lower= query.lower()
    if any(keyword in query_lower for keyword in  web_search_keywords):
        return 'web search'
    if doc_score >= 0.7:
        print(f"Routing: DOCUMENT QA (score={doc_score})")
        return "document_qa"
    elif doc_score <= 0.3:
        print(f"Routing: WEB SEARCH (score={doc_score})")
        return "web_search"
    else:
        print(f"Routing: HYBRID (score={doc_score})")
        return "hybrid_search"