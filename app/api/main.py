from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
from app.api.imei_service import check_imei_from_api
from app.api.models import ImeiRequest
from app.db.crud import add_user_to_white_list
from app.db.model import Session
from app.db.session import get_db

app = FastAPI()

router = APIRouter()

@router.post("/api/check-imei")
async def check_imei(request: ImeiRequest):
    imei = request.imei
    token = request.token

    imei_info = await check_imei_from_api(imei, token)

    return imei_info.json()

@app.post("/api/add_user/")
async def add_user(user_id: int, username: str, db: Session = Depends(get_db)):
    try:
        new_user = add_user_to_white_list(db, user_id, username)
        return {"message": "User added successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(router)
