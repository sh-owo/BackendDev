from fastapi import APIRouter, HTTPException, Header
from app.database import notes_collection

router = APIRouter()


@router.post("/create_note/")
def create_note(title: str, content: str, user_id: str = Header(None)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    note = {
        "title": title,
        "content": content,
        "owner": user_id
    }
    notes_collection.insert_one(note)
    return {"message": "Note created successfully"}


@router.get("/get_notes/")
def get_notes(user_id: str = Header(None)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    notes = []
    for note in notes_collection.find({"owner": user_id}):
        notes.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"]
        })
    return notes


@router.delete("/delete_note/{note_id}")
def delete_note(note_id: str, user_id: str = Header(None)):
    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    result = notes_collection.delete_one({"_id": note_id, "owner": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")

    return {"message": "Note deleted successfully"}
