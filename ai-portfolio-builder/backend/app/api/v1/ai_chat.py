from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/chat")
async def chat_with_portfolio(
    slug: str, 
    query: str, 
    db: Session = Depends(get_db)
):
    # This is a public endpoint, so no current_user dependency
    return await AIService.generate_response(db, slug, query)
