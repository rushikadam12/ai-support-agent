from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from config import GEMINI_API_KEY
from utils.logger import log_info
from langchain_core.runnables import RunnableLambda
from typing import Any


support_template = """
You are an AI Customer Support Assistant for an online electronics shop called ElectroMart.
Answer customer questions politely and clearly. 
If you don’t know the answer, say so and suggest contacting human support.

Customer Question: {question}
Answer:
"""

# prompt=PromptTemplate(input_variables=["question"],template=support_template)

# memory=ConversationBufferMemory(memory_key="chat_history",return_messages=True)

# llm=ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",
#     api_key=GEMINI_API_KEY,
#     temperature=0.5
# )

# cha_chain=ConversationalRetrievalChain.from_llm(
#     llm=llm
    
# )


def format_docs(docs):
    if not isinstance(docs, list):
        raise TypeError(f"Expected list of Documents, got {type(docs)}: {docs}")
    return "\n\n".join(getattr(doc, "page_content", str(doc)) for doc in docs)

def get_context(retriever,question):
    docs=retriever.get_relevant_documents(question)
    if not docs:
        return "No relevant documents found."
    return format_docs(docs)

def create_qa_chain():

    prompt = hub.pull("rlm/rag-prompt")


    llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.5
    )
    
    # qa_chain=(
    #     {
    #         "context":RunnablePassthrough(),    
    #         "question":RunnablePassthrough()
    #     }
    #     |prompt
    #     |llm
    #     |StrOutputParser()
    # )
    
    qa_chain = RunnableLambda(
        lambda inputs: llm.invoke(prompt.format(context=inputs["context"], question=inputs["question"]))
    )

    return qa_chain


def get_agent_response(VectorStore:Any,question:str):
    log_info("type:",type(VectorStore))
    
    retriever=VectorStore.as_retriever()
    log_info(type(retriever))      

    docs = retriever.get_relevant_documents(question)
    log_info(f"Number of docs retrieved: {len(docs)}")

    context = format_docs(docs) if docs else "No relevant documents found."
    log_info("Context string:", context[:100])

    inputs = {"context": context, "question": question}
    log_info("LLM inputs:", inputs)

    rag_chain= create_qa_chain()
    result=rag_chain.invoke(inputs)

    log_info(result,"<----------get_agent_response()")
    return result.content if hasattr(result, "content") else str(result)