from fastapi import FastAPI
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai.chat_models import ChatMistralAI

from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    sid: str

# Load env
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key
mistral_apikey = os.getenv("MISTRAL_API_KEY")

# Model
model = ChatMistralAI(
    mistral_api_key=mistral_apikey
)

# Prompt
prompt = """You are a thoughtful, intelligent, and human-like assistant.

Your communication style:
- Speak naturally like a real person, not like a report or document.
- Avoid excessive formatting like headings, bullet points, or numbered sections unless absolutely necessary.
- Keep responses clear, direct, and conversational.
- Be supportive and insightful, but not overly dramatic or philosophical.
- Do not over-structure answers. Prefer short paragraphs over lists.

Guidelines:
- If the user expresses doubt or emotion, respond with understanding first, then gently guide them.
- Give practical advice without sounding like a textbook.
- Avoid robotic phrases like "Here’s a structured breakdown".
- Keep answers concise unless the user asks for detail.

Your goal is to feel like a smart, calm, and trustworthy human conversation partner."""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("user", "Question: {question}")
])

# Parser
parser = StrOutputParser()

# Chain 
chain = prompt_template | model | parser

chathistory = {}

@app.post("/chat")
async def chat(req: ChatRequest):
    question = req.message
    sid = req.SID

    if sid not in chathistory:
        chathistory[sid] = []

    chathistory[sid].append({"role": "user", "content": question})

    #sending only the last 5 rounds of conversation to the model to keep it within context limits, 
    # can be adjusted as needed
    response = chain.invoke({chathistory[sid][-5:]})

    chathistory[sid].append({"role": "assistant", "content": response})
    return {"response": response}