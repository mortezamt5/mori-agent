from fastapi import FastAPI , HTTPException
from typing import Literal
from pydantic import BaseModel
from mori_agent.agent import generate_response
import requests
app = FastAPI(
    title= "Mori Agent API",
    version="0.1.0"
)
class ChatMessage(BaseModel):
    role: Literal["user" , "assistant"]
    content: str

class ChatRequest(BaseModel):
    message: str
    history : list[ChatMessage] = []

@app.get("/health")
def health():
    return {"status": "OK" , "agent": "mori"}

@app.post("/chat")
async def chat(request: ChatRequest):
    messages = [
        {"role": item.role , "content": item.content   }
        for item in request.history
    ]
    messages.append({
        "role": "user",
        "content": request.message
    })
    
    try:
        reply = await generate_response(messages)
        return {
            "thinking": reply["thinking"],
            "content": reply["content"],
            "history": messages + [
                {"role": "assistant", "content": reply["content"]}
            ],
        }
    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Mori_Agent connection failed : {error} "
        )
    