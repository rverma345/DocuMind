import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def load_documents(file_paths):
    """
    Accepts a list of file paths (PDFs) and loads them.
    """
    all_docs = []
    for path in file_paths:
        loader = PyPDFLoader(file_path=path)
        docs = loader.load()
        for d in docs:
            d.metadata.setdefault('source', os.path.basename(path))
        all_docs.extend(docs)
    return all_docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents=docs)
    return chunks


def embed_and_store(chunks, persist_dir='vector_store/'):
    model = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=model,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    return vectorstore


def ingest_documents(file_paths, persist_dir='vector_store/'):
    """
    Full ingestion pipeline:
    - Takes a list of PDF file paths.
    - Loads and splits them.
    - Embeds and stores them into ChromaDB.
    """
    docs = load_documents(file_paths)
    chunks = split_documents(docs)
    vectorstore = embed_and_store(chunks, persist_dir)
    return vectorstore
