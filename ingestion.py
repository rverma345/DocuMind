# This is a utility file where all the code for document ingestion and helper functions goes 
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


def document_loading(path):
    loader=PyPDFLoader(file_path=path)
    docs=loader.load()
    for d in docs:
        d.metadata.setdefault('source',os.path.basename(path))
    return docs
def chunking(docs):
    chunker=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks=chunker.split_documents(documents=docs)
    return chunks

def indexing(path : str):
    