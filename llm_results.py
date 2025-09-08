from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
parser = StrOutputParser()

llm = ChatOpenAI(
    model='gpt-5-mini-2025-08-07',
    temperature=0.3
)

def generate_result(query, context):
    prompt = PromptTemplate(
        input_variables=["query", "context"],
        template=(
            "You are an intelligent assistant.\n"
            "Answer the following query based only on the given context.\n\n"
            "Query: {query}\n\n"
            "Context:\n{context}\n\n"
            "Answer clearly and concisely.\n"
            "If you don't know from the context, just say 'I don't know'.\n\n"
            "[Sources: document name / web link]"
        )
    )
    result_chain = prompt | llm | parser
    return result_chain.invoke({"query": query, "context": context})
