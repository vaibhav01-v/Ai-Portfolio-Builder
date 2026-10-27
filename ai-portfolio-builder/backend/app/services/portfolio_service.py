from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.portfolio import Portfolio
from app.models.project import Project
from app.schemas.portfolio import PortfolioCreate, ProjectCreate
import uuid

class PortfolioService:
    @staticmethod
    def create_portfolio(db: Session, user_id: uuid.UUID, data: PortfolioCreate) -> Portfolio:
        # Check if slug is taken
        existing = db.query(Portfolio).filter(Portfolio.slug == data.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already in use")
            
        portfolio = Portfolio(
            **data.model_dump(),
            user_id=user_id
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        return portfolio

    @staticmethod
    def get_user_portfolios(db: Session, user_id: uuid.UUID):
        return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    @staticmethod
    def update_portfolio(db: Session, portfolio_id: uuid.UUID, user_id: uuid.UUID, data: PortfolioCreate):
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        if portfolio.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this portfolio")
            
        for key, value in data.model_dump().items():
            setattr(portfolio, key, value)
            
        db.commit()
        db.refresh(portfolio)
        return portfolio

    @staticmethod
    def add_project(db: Session, portfolio_id: uuid.UUID, user_id: uuid.UUID, data: ProjectCreate):
        # Verify ownership of portfolio before adding project
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio or portfolio.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to add project to this portfolio")
            
        project = Project(
            **data.model_dump(),
            portfolio_id=portfolio_id
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
