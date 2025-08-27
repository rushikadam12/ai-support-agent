from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import prompt
from langchain.chains import retrieval_qa
from pypdf import PdfReader
from utils.logger import log_info
import os
import config


def extract_text_from_pdf(path:str):
    cwd=os.getcwd()
    log_info(cwd)
    pdf_path=os.path.join(cwd,"services","dm-series_privacy_notice.pdf")
    log_info(pdf_path)

    pdf_reade_buffer=PdfReader(pdf_path)
    text=""

    for page in pdf_reade_buffer.pages:
        text+=page.extract_text()+"\n"
    
    return text

def split_text(text):
    chunks=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    return chunks.split_text(text)




