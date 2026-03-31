from fastapi import FastAPI
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai.chat_models import ChatMistralAI

from pydantic import BaseModel

# ------------------ Request Model ------------------
class ChatRequest(BaseModel):
    message: str
    sid: str   # ✅ consistent naming

# ------------------ Load ENV ------------------
load_dotenv()

mistral_apikey = os.getenv("MISTRAL_API_KEY")
if not mistral_apikey:
    raise ValueError("MISTRAL_API_KEY is not set")

# ------------------ App Init ------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Model ------------------
model = ChatMistralAI(
    mistral_api_key=mistral_apikey
)

# ------------------ Prompt ------------------
prompt = """You are a thoughtful, intelligent, and human-like assistant.

Your communication style:
- Speak naturally like a real person
- Avoid excessive formatting
- Keep responses conversational and clear
- Be helpful but not robotic
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("user", "Conversation:\n{question}")
])

parser = StrOutputParser()
chain = prompt_template | model | parser

# ------------------ Memory ------------------
chathistory = {}

# ------------------ Endpoint ------------------
@app.post("/chat")
async def chat(req: ChatRequest):
    question = req.message
    sid = req.sid   # ✅ fixed

    if sid not in chathistory:
        chathistory[sid] = []

    # store user message
    chathistory[sid].append({"role": "user", "content": question})

    # take last 5 messages
    history = chathistory[sid][-5:]

    # format conversation
    conversation = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation += f"{role}: {msg['content']}\n"

    # invoke model
    response = chain.invoke({
        "question": conversation + f"User: {question}"
    })

    # store response
    chathistory[sid].append({"role": "assistant", "content": response})

    return {"response": response}