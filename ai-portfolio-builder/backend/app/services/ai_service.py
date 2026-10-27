import requests
import json
from fastapi import HTTPException
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.project import Project

class AIService:
    @staticmethod
    def _get_portfolio_context(db: Session, slug: str) -> str:
        portfolio = db.query(Portfolio).filter(
            Portfolio.slug == slug, 
            Portfolio.is_published == True
        ).first()
        
        if not portfolio:
            return ""

        projects = db.query(Project).filter(
            Project.portfolio_id == portfolio.id, 
            Project.is_visible == True
        ).all()

        project_list = "\n".join([
            f"- {p.name}: {p.description} (Tech: {', '.join(p.tech_stack or [])})" 
            for p in projects
        ])

        return (
            f"User Name/Title: {portfolio.title}\n"
            f"Bio: {portfolio.bio}\n"
            f"Projects:\n{project_list}"
        )

    @staticmethod
    async def generate_response(db: Session, slug: str, user_query: str) -> dict:
        context = AIService._get_portfolio_context(db, slug)
        if not context:
            raise HTTPException(status_code=404, detail="Portfolio not found or not published")

        system_prompt = (
            "You are a professional AI Portfolio Assistant. You must respond ONLY in JSON format. "
            "The JSON must have a single key 'response' containing the answer.\n"
            "STRICT RULES:\n"
            "1. Use ONLY the provided context. Do NOT invent skills.\n"
            "2. If information is missing, set 'response' to 'I am sorry, that information is not available.'\n"
            "3. Be professional and concise.\n\n"
            f"CONTEXT:\n{context}"
        )

        try:
            response = requests.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": f"{system_prompt}\n\nUser Question: {user_query}",
                    "stream": False,
                    "format": "json", # Forces Ollama to return valid JSON
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 256
                    }
                },
                timeout=30
            )
            response.raise_for_status()
            # Parse the string response into a real JSON object
            return json.loads(response.json().get("response", '{"response": "Error generating response"}'))
        except Exception as e:
            print(f"Ollama Error: {e}")
            raise HTTPException(status_code=503, detail="AI service is currently unavailable")
