from fastapi import FastAPI
from fastapi.responses import FileResponse
from App.Routers import note

app = FastAPI()

app.include_router(note.router)

@app.get("/")
async def read_root():
    return FileResponse("public/index.html")

@app.get("/style.css")
async def get_css():
    return FileResponse("public/style.css")