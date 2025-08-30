import uvicorn
from fastapi import FastAPI
from routes import chat

app=FastAPI(
    title="Chat API",
    description="AI_chat_app swagger docs",
    version="1.0.0",
    contact={
        "name": "RK",
    })

app.include_router(chat.router)

# TODO:create vector db chatbot here which read policy from pdf and answer here


@app.get("/")
def Home():
    return {"message":"server is running"}

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=5000,reload=True)