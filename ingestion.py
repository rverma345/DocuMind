# This is a utility file where all the code for document ingestion and helper functions goes 
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def load_documents(path):
    loader=PyPDFLoader(file_path=path)
    docs=loader.load()
    for d in docs:
        d.metadata.setdefault('source',os.path.basename(path))
    return docs
def split_documents(docs):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks=splitter.split_documents(documents=docs)
    return chunks

def embed_and_store(chunks,persist_dir='vector_store/'):
    model=OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore=Chroma.from_documents(
        documents=chunks,
        embedding=model,
        persist_directory=persist_dir
    )
    vectorstore.persist()
    return vectorstore

# 4. End-to-end ingestion pipeline

def ingest_documents(folder_path='data/',persist_dir='vector_store/'):
    docs=load_documents(folder_path)
    chunks=split_documents(docs)
    vectorstore=embed_and_store(chunks,persist_dir)
    return vectorstore
    