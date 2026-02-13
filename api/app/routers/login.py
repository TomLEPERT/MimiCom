import os
from fastapi import APIRouter, HTTPException
from ..models.login import LoginPayload, UpdateCredsPayload
from .env_store import get_creds, update_creds
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginPayload):
    username, password = get_creds()
    if payload.username == username and payload.password == password:
        return {"ok": True}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/current")
async def current():
    username, _ = get_creds()
    return {"username": username}

@router.post("/update")
def update(payload: UpdateCredsPayload):
    username, password = get_creds()
    
    if payload.current_username != username or payload.current_password != password:
        raise HTTPException(status_code=401, detail="Invalid current credentials")
    
    if not payload.new_username or not payload.new_password:
        raise HTTPException(status_code=400, detail="New credentials cannot be empty")
    
    update_creds = (payload.new_username, payload.new_password)
    os.environ["APP_USERNAME"] = payload.new_username
    os.environ["APP_PASSWORD"] = payload.new_password
    
    return {"ok": True}