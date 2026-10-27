# 📋 Production Readiness Checklist

## 🔐 Security Hardening
- [ ] **SSL/TLS:** Deploy behind Nginx/Caddy with Let's Encrypt certificates.
- [ ] **Secrets Management:** Move `.env` variables to a secure vault (AWS Secrets Manager / HashiCorp Vault).
- [ ] **Cookie Settings:** Ensure `secure=True` and `httpOnly=True` are enabled for all session cookies.
- [ ] **CORS:** Change `allow_origins=["*"]` to only the specific production frontend domain.
- [ ] **Rate Limiting:** Implement `slowapi` or Nginx rate limiting on `/api/v1/auth/login` and `/api/v1/chat`.

## 🗄️ Database & Storage
- [ ] **Backups:** Configure automated daily backups for PostgreSQL.
- [ ] **Indexing:** Verify indexes on `users.email` and `portfolios.slug`.
- [ ] **Migrations:** Ensure `alembic upgrade head` is part of the deployment pipeline.

## 🤖 AI Infrastructure
- [ ] **GPU Acceleration:** Ensure the Ollama container has access to NVIDIA GPUs via `nvidia-container-toolkit`.
- [ ] **Model Quantization:** Use 4-bit quantized models to reduce VRAM usage.
- [ ] **Timeout Tuning:** Adjust FastAPI timeout settings for longer AI response times.

## 📈 Monitoring
- [ ] **Logging:** Connect `app.log` to a centralized system (ELK Stack / Sentry).
- [ ] **Health Checks:** Implement `/health` endpoints for Docker/K8s health checks.
