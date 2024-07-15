from fastapi import APIRouter, HTTPException, Form
from bson import ObjectId
from App.database import notes_collection

router = APIRouter()

@router.post("/create_note/")
async def create_note(
    title: str = Form(...),
    content: str = Form(...)
):
    note = {
        "title": title,
        "content": content
    }
    notes_collection.insert_one(note)
    return {"message": "Note created successfully"}

@router.get("/get_notes/")
async def get_notes():
    notes = []
    for note in notes_collection.find():
        notes.append({"id": str(note["_id"]), "title": note["title"], "content": note["content"]})
    return notes

@router.delete("/delete_note/{note_id}")
async def delete_note(note_id: str):
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}