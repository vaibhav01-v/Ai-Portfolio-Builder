from fastapi import APIRouter, Depends, Response, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserOut, TokenResponse
from app.core.security import create_session_token

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserCreate, response: Response, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    
    # Create secure session token
    session_token = create_session_token()
    
    # In a production app, we would store this token in a Redis/DB session table
    # For this MVP, we are implementing the cookie flow
    response.set_cookie(
        key="session_id", 
        value=session_token, 
        httponly=True, 
        secure=True, # Set to False in local dev if not using HTTPS
        samesite="lax",
        max_age=3600 * 24 # 24 hours
    )
    
    return TokenResponse()

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}
