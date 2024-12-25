from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.response_generator import chat, get_rag_engine

router = APIRouter()

class userResponse(BaseModel):
    session_id: str
    userInput: str
    
rag_engine = get_rag_engine()

@router.post("/chat")
async def chat_function(body: userResponse):
    try:
        response = chat(body.userInput, rag_engine)
        return {"code": 200, "message": "Response successfully generated.", "response": response, "metadata": {}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing input: {e}")
    