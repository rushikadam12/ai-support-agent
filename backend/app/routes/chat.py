from fastapi import APIRouter,Response
from models.query import ChatRequest,ChatResponse,FileUpload
from services.faq_service import look_for_faq
from services.vector_embedding_pipeline import extract_text_from_pdf,split_text,create_vectorstore
from services.agent_service import get_agent_response

from utils.file_operations import save_file
import asyncio
import shutil, uuid
from utils.logger import log_info
from fastapi import UploadFile

router=APIRouter()

VECTORSTORES = {}
CHAT_HISTORY = {}

@router.post("/chat",)
async def chat_endpoint(request:ChatRequest):
    try:
        session_id=request.session_id
        question=request.question
        log_info(session_id)
        log_info("vectore_store==>",VECTORSTORES)

        if session_id not in VECTORSTORES:
            return {"error":"session id not found","message":"invalid session id"},400
        
        VectorStore=VECTORSTORES[session_id]

        
        log_info(VectorStore)
                
        if session_id not in CHAT_HISTORY:
            CHAT_HISTORY[session_id] = []

        CHAT_HISTORY[session_id].append({"role": "user", "content": question})
        log_info("before_get_agent_response")
        
        response= get_agent_response(VectorStore,question)

        log_info(response)

        CHAT_HISTORY[session_id].append({"role": "assistant", "content": response})
        
        return {"question":question,"llm_response":response,"chat_history":CHAT_HISTORY[session_id]},200
    
    except Exception as error:  
        log_info(f"error--------->{error}")
        return {"message":"something went wrong","error":str(error)},500

@router.post("/upload_pdf")
async def upload_pdf_file(file:UploadFile):
    try:
        session_id=str(uuid.uuid4())
        file_path=save_file(file,session_id)

        text=extract_text_from_pdf(file_path)
        chunks=split_text(text)
        VectorStore=create_vectorstore(chunks)

        VECTORSTORES[session_id]=VectorStore
        CHAT_HISTORY[session_id]=[]

        log_info("info---------------->")
        log_info(VectorStore)
        log_info(CHAT_HISTORY)

        return {"session_id":session_id,"message":"file_upload successfully!"},202

    except Exception as e:
        log_info(f"error--------->{e}")
        return {"status":500,"message":"failed","content":str(e)}