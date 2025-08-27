from fastapi import APIRouter,Response
from models.query import ChatRequest,ChatResponse,FileUpload
from services.faq_service import look_for_faq
from services.agent_service import get_agent_response
from services.vector_embedding_pipeline import extract_text_from_pdf
import asyncio
from utils.logger import log_info

router=APIRouter()

@router.post("/chat",response_model=ChatResponse)
async def chat_endpoint(request:ChatRequest):
    try:
        faq_answer=look_for_faq(question=request.question)
        log_info(f"faq_answer----------->{faq_answer}")
        if faq_answer:
            return {"answer":faq_answer,"escalate":False}

        response= get_agent_response(question=request.question)

        return ChatResponse(answer=response)
    
    except Exception as error:
        log_info(f"error--------->{error}")
        return ChatResponse(answer=str(error))

@router.get("/upload-pdf")
async def upload_pdf_file():
    try:
        text=await asyncio.to_thread(extract_text_from_pdf,"")
        log_info(text)
        return FileUpload(status=201,message="success",content=text)
    except Exception as e:
        log_info(f"error--------->{e}")
        return FileUpload(status=500,message="failed",content=str(e))