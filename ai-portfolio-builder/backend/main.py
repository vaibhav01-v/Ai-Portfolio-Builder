from fastapi import FastAPI
from app.api.v1 import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Portfolio Builder API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to AI Portfolio Builder API"}
