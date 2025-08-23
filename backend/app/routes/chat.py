from fastapi import APIRouter
from models.query import ChatRequest,ChatResponse
from services.faq_service import look_for_faq
from services.agent_service import get_agent_response
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


