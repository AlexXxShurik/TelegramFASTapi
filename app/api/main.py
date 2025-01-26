import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from app.db.crud import add_user_to_white_list, get_all_white_list_users
from app.db.session import get_db
from app.db.model import Session
from app.api.imei_service import check_imei_from_api
from app.api.models import ImeiRequest, UserRequest

app = FastAPI()

load_dotenv()
SANDBOX_API_TOKEN = os.getenv("SANDBOX_API_TOKEN")


def verify_token(token: str):
    if token != "Bearer " + SANDBOX_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@app.post("/api/check-imei")
async def check_imei(request: ImeiRequest):
    verify_token(request.token)
    imei = request.imei
    imei_info = await check_imei_from_api(imei)
    return imei_info.json()


@app.post("/api/add_user")
async def add_user(request: UserRequest, db: Session = Depends(get_db)):
    """Добавление пользователя в белый список"""
    verify_token(request.token)
    white_list_users = get_all_white_list_users(db)
    white_list_user_ids = [user.user_id for user in white_list_users]

    if request.user_id in white_list_user_ids:
        raise HTTPException(status_code=400, detail="User already in the whitelist.")

    try:
        new_user = add_user_to_white_list(db, request.user_id, request.username)
        return {"message": "User added successfully", "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
