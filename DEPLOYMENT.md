# 🚀 Deployment Guide

## Quick Start (Local)

### 1. Prerequisites
```bash
python -3.10 --version  # Should be 3.10+
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
# Backend runs on http://127.0.0.1:8000
```

### 3. Frontend Setup (New Terminal)
```bash
cd frontend
python -m http.server 3000
# Frontend runs on http://127.0.0.1:3000
```

### 4. Access
Open browser: **http://127.0.0.1:3000**

---

## Docker Deployment

### Build & Run
```bash
docker-compose up -d
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Check Status
```bash
docker-compose ps
docker-compose logs -f backend
```

### Stop
```bash
docker-compose down
```

---

## Cloud Deployment (Railway.app)

### 1. Connect Repository
- Push code to GitHub
- Connect repo to Railway.app
- Auto-deploy from Dockerfile

### 2. Environment Variables
```
PORT=8000
PYTHONUNBUFFERED=1
```

### 3. Start Command
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Production Checklist

- ✅ Backend: FastAPI (Production-ready)
- ✅ Frontend: Static files (Optimized)
- ✅ Model: YOLOv5 (Trained, Quantized)
- ✅ Dependencies: Locked (requirements.txt)
- ✅ Environment: Containerized (Docker)
- ✅ Monitoring: Logs enabled
- ✅ Security: CORS enabled

---

## Troubleshooting

### Backend not starting
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Port already in use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn main:app --port 9000
```

### API connection error
- Check backend is running: http://127.0.0.1:8000
- Check firewall settings
- Verify API_URL in frontend/app.js

---

## Performance Tips

- Use GPU if available: Update `device=cuda` in main.py
- Cache model after first load
- Optimize image size before upload
- Use CDN for static files in production

---

## Support

For issues, check:
1. Backend logs: `docker-compose logs backend`
2. Frontend console: F12 → Console tab
3. API docs: http://localhost:8000/docs
