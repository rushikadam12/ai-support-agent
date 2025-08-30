from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import prompt
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from pypdf import PdfReader
from langchain import hub
from utils.logger import log_info
import os
import config


def extract_text_from_pdf(path:str):
    pdf_reade_buffer=PdfReader(path)
    text=""

    for page in pdf_reade_buffer.pages:
        text+=page.extract_text()+"\n"
    
    return text

def split_text(text):
    chunks=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    return chunks.split_text(text)

def create_vectorstore(chunks):
    embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001",
    google_api_key=config.GEMINI_API_KEY)
    return Chroma.from_texts(chunks,embedding=embedding,persist_directory="chroma_store")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# def create_qa_chain(vectorstore):

#     prompt = hub.pull("rlm/rag-prompt")

#     retriever=vectorstore.as_retriever()

#     llm=ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     api_key=config.GEMINI_API_KEY,
#     temperature=0.5
#     )

#     qa_chain=(
#         {
#             "context":retriever|format_docs,    
#             "question":RunnablePassthrough()
#         }
#         |prompt
#         |llm
#         |StrOutputParser()
#     )
#     return qa_chain

# def start_query():
    
#     text=extract_text_from_pdf(r"C:\Users\Rushikesh Kadam\OneDrive\Documents\code_space\ai-support-agent\backend\app\services\dm-series_privacy_notice.pdf")
#     chunks=split_text(text)
#     VectorStore=create_vectorstore(chunks)
#     qa_chain=create_qa_chain(VectorStore)

#     query="which company policy is this?"

#     result=qa_chain.invoke(query)
#     return result


