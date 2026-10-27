from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str
    tech_stack: Optional[List[str]] = None
    link: Optional[str] = None
    is_visible: bool = True

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: UUID
    
    class Config:
        from_attributes = True

class PortfolioBase(BaseModel):
    title: str
    template_id: str = "default"
    bio: Optional[str] = None
    is_published: bool = False
    slug: str

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioOut(PortfolioBase):
    id: UUID
    user_id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True
