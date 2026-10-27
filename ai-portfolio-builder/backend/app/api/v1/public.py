from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db
from fastapi import Depends
from app.models.portfolio import Portfolio
from app.models.project import Project
from app.schemas.portfolio import PortfolioOut, ProjectOut

router = APIRouter()

@router.get("/portfolio/{slug}", response_model=PortfolioOut)
def get_public_portfolio(slug: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(
        Portfolio.slug == slug, 
        Portfolio.is_published == True
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Portfolio not found or not published"
        )
    return portfolio

@router.get("/portfolio/{slug}/projects", response_model=List[ProjectOut])
def get_public_projects(slug: str, db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(
        Portfolio.slug == slug, 
        Portfolio.is_published == True
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Portfolio not found or not published"
        )
        
    return db.query(Project).filter(
        Project.portfolio_id == portfolio.id, 
        Project.is_visible == True
    ).all()
