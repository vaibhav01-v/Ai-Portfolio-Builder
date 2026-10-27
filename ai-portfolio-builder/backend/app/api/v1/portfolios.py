from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.db.session import get_db
from app.api.v1.dependencies import get_current_user
from app.services.portfolio_service import PortfolioService
from app.schemas.portfolio import PortfolioCreate, PortfolioOut, ProjectCreate, ProjectOut
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PortfolioOut, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    data: PortfolioCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return PortfolioService.create_portfolio(db, current_user.id, data)

@router.get("/", response_model=List[PortfolioOut])
def list_portfolios(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return PortfolioService.get_user_portfolios(db, current_user.id)

@router.put("/{portfolio_id}", response_model=PortfolioOut)
def update_portfolio(
    portfolio_id: UUID, 
    data: PortfolioCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return PortfolioService.update_portfolio(db, portfolio_id, current_user.id, data)

@router.post("/{portfolio_id}/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def add_project(
    portfolio_id: UUID, 
    data: ProjectCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return PortfolioService.add_project(db, portfolio_id, current_user.id, data)
