from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from app.routers import note, gpt
from app.database import users_collection

app = FastAPI()

# 라우터 등록
app.include_router(note.router, prefix="/notes")
app.include_router(gpt.router, prefix="/gpt")


@app.post("/signup")
def signup(id: str = Header(None), passwd: str = Header(None)):
    if id is None or passwd is None:
        raise HTTPException(status_code=400, detail="ID or password is None")

    if users_collection.find_one({"id": id}):
        raise HTTPException(status_code=400, detail="ID already exists")

    users_collection.insert_one({"id": id, "pw": passwd})

    return {'status': 200, 'message': 'success'}


@app.get("/check")
def check(id: str = Header(None), passwd: str = Header(None)):
    user = users_collection.find_one({"id": id, "pw": passwd})
    if user:
        return {'status': 200, 'message': 'success'}
    else:
        raise HTTPException(status_code=400, detail="ID or password is wrong")


@app.post("/logout")
def logout(id: str = Header(None)):
    if id is None:
        raise HTTPException(status_code=400, detail="ID is required")

    # 로그아웃 처리 로직 (세션 관리 필요 시 구현)
    return {'status': 200, 'message': 'Logged out successfully'}


@app.get("/")
async def read_root():
    return FileResponse("public/index.html")


@app.get("/style.css")
async def get_css():
    return FileResponse("public/style.css")
