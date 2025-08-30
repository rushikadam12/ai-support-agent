from pydantic import BaseModel,Field,field_validator
from typing import Any,Optional
from fastapi import UploadFile

class ChatRequest(BaseModel):
      question:str=Field(...,min_length=5)
      session_id:str=Field(...,min_length=5)

      @field_validator("question")
      def questions_should_not_empty(cls,v:str):
            if not v.strip():
                  raise ValueError("question field is required")
            return v

      @field_validator("session_id")
      def session_should_not_empty(cls,v:str):
            if not v.strip():
                  raise ValueError("session_id field is required")
            return v


class ChatResponse(BaseModel):
      answer:str
      
      @field_validator("answer")
      def questions_should_not_empty(cls,v:str):
            if not v.strip():
                  raise ValueError("answer field is required")
            return v

class FileUpload(BaseModel):
    question: str = Field(..., min_length=5)
    file: Optional[UploadFile] = None

    @field_validator("question")
    def question_should_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Question field is required")
        return v

    @field_validator("file")
    def validate_file(cls, file: Optional[UploadFile]):
        if file is None:
            raise ValueError("File is required")
        
        
        allowed_extensions = {".pdf", ".txt", ".docx"}
        filename = file.filename.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"File must be one of: {', '.join(allowed_extensions)}")

        return file