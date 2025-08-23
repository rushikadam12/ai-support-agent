import uvicorn
from fastapi import FastAPI
from routes import chat

app=FastAPI(title="Chat API")

app.include_router(chat.router)

@app.get("/")
def Home():
    return {"message":"server is running"}

if __name__=="__main__":
    uvicorn.run("" \
    "main:app",host="0.0.0.0",port=5000,reload=True)