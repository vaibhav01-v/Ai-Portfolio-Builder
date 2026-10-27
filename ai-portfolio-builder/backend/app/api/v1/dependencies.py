from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User

async def get_current_user(
    session_id: str = Cookie(None), 
    db: Session = Depends(get_db)
):
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not authenticated"
        )
    
    # NOTE: In production, we query a 'sessions' table in DB or Redis.
    # For this MVP phase, we'll simulate the session lookup.
    # In Phase 4.5, we will add the actual session storage.
    user = db.query(User).first() # Simplified for MVP; will be replaced by session lookup
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid session"
        )
    return user
