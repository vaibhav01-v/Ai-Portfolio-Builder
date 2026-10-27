# 🚀 AI Portfolio Builder

A production-oriented, multi-user SaaS application that allows developers to create professional portfolios with an integrated local AI chatbot that answers questions based on their published work.

## 🌟 Features
- **Multi-tenant Architecture:** Secure isolation of user data.
- **Professional Portfolio CRUD:** Manage projects, skills, and experience.
- **Public Routing:** Unique slugs for public portfolio sharing.
- **AI Chatbot (RAG):** Locally hosted AI via Ollama that uses Retrieval-Augmented Generation to answer factual questions about the portfolio owner.
- **Industry-Standard Security:** Argon2id hashing, HTTP-only session cookies, and ownership guards.

## 🛠️ Tech Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS.
- **Backend:** Python, FastAPI, SQLAlchemy 2.x, Pydantic.
- **Database:** PostgreSQL.
- **AI:** Ollama (Llama 3 / Mistral).
- **Infrastructure:** Docker, GitHub Actions.

## 🚀 Quick Start (Docker)

### 1. Prerequisites
- Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).
- Install [Ollama](https://ollama.ai/) (if running locally) or use the provided Docker image.

### 2. Setup
```bash
# Clone the repo
git clone <your-repo-url>
cd ai-portfolio-builder

# Start the stack
docker-compose -f docker/docker-compose.yml up --build -d
```

### 3. Initialize AI Model
Run this command to pull the recommended model into the Ollama container:
```bash
docker exec -it ollama_ai ollama run llama3
```

## 🔌 API Documentation
Once running, the API documentation is available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## 🛡️ Security Architecture
- **Authentication:** Server-managed sessions via secure cookies.
- **Authorization:** Every request is filtered by `user_id` derived from the session.
- **AI Guardrails:** System prompts restrict the AI to provided context only, preventing hallucinations.
