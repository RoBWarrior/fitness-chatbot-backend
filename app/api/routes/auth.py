from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
from app.services.db_helpers import create_user, get_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserAuth(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserAuth):
    # Check if user exists
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Save user
    user_id = create_user(user.username, hashed_password)
    if not user_id:
        raise HTTPException(status_code=500, detail="Could not create user")
        
    return {"status": "success", "user_id": user_id, "username": user.username}

@router.post("/login")
async def login(user: UserAuth):
    # Fetch user
    db_user = get_user(user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    # verify password
    # In 'get_user', order in select * is:
    # 0: user_id, 1: username, 2: password_hash, 3: created_at 
    # Wait, let's look at schema:
    # 0: user_id (SERIAL)
    # 1: username (VARCHAR)
    # 2: created_at (TIMESTAMP)
    # 3: password_hash (VARCHAR) -> Because we ALTER TABLE ADD COLUMN
    stored_hash = db_user[3]
    
    if not pwd_context.verify(user.password, stored_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    return {"status": "success", "user_id": db_user[0], "username": db_user[1]}
