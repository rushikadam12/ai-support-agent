from pydantic import BaseModel,Field,field_validator

class ChatRequest(BaseModel):
      question:str=Field(...,min_length=5)
      
      @field_validator("question")
      def questions_should_not_empty(cls,v:str):
            if not v.strip():
                  raise ValueError("Question field is required")
            return v



class ChatResponse(BaseModel):
      answer:str
      
      @field_validator("answer")
      def questions_should_not_empty(cls,v:str):
            if not v.strip():
                  raise ValueError("answer field is required")
            return v