# Adding a CSRF protection helper
import secrets
from fastapi import Request, HTTPException, status

def validate_csrf_token(request: Request, token: str):
    # Simplified CSRF check for MVP
    if not token or token != request.headers.get("X-CSRF-Token"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="CSRF token missing or invalid"
        )
