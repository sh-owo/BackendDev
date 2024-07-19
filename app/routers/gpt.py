from fastapi import APIRouter, HTTPException, Header
from app.database import notes_collection
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GPT_KEY")

router = APIRouter()

@router.post("/chat/")
def chat_with_gpt(prompt: str, user_id: str = Header(None)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        message = response['choices'][0]['message']['content']

        # 대화 기록 저장
        notes_collection.insert_one({"prompt": prompt, "response": message, "owner": user_id, "type": "chat"})

        return {"response": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat_history/")
def get_chat_history(user_id: str = Header(None)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    history = []
    for record in notes_collection.find({"owner": user_id, "type": "chat"}):
        history.append({
            "id": str(record["_id"]),
            "prompt": record["prompt"],
            "response": record["response"]
        })
    return history
