from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY
from utils.logger import log_info


support_template = """
You are an AI Customer Support Assistant for an online electronics shop called ElectroMart.
Answer customer questions politely and clearly. 
If you don’t know the answer, say so and suggest contacting human support.

Customer Question: {question}
Answer:
"""

prompt=PromptTemplate(input_variables=["question"],template=support_template)

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.5
)

def get_agent_response(question:str):
    
    resp= llm.invoke(prompt.format(question=question))
    log_info(resp,"<----------get_agent_response()")
    return resp.content