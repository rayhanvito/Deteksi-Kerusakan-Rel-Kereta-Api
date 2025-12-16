# 🚀 Railway + Vercel Deployment Guide

Deploy backend to Railway dan frontend ke Vercel untuk production!

---

## ⚙️ Persiapan

### 1. Setup Railway (Backend)

#### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

#### Step 2: Connect GitHub Repository
1. Click "New Project" → "Deploy from GitHub repo"
2. Select: `rayhanvito/Deteksi-Kerusakan-Rel-Kereta-Api`
3. Railway akan auto-detect Python project

#### Step 3: Configure Environment
Railway settings:
```
PORT=8000
PYTHONUNBUFFERED=1
```

The `Procfile` file will tell Railway how to start:
```
web: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Step 4: Deploy
- Railway auto-deploys on push to main
- Get your backend URL (e.g., `https://yourproject-production.up.railway.app`)

---

## 🎨 Persiapan Vercel (Frontend)

### 1. Setup Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your project

#### Step 1: Create Vercel Project
1. Click "Add New..." → "Project"
2. Select: `rayhanvito/Deteksi-Kerusakan-Rel-Kereta-Api`
3. Framework: "Other" (HTML/CSS/JS)
4. Root Directory: `frontend`

#### Step 2: Configure Environment Variables
Go to Project Settings → Environment Variables:

```
Name: VITE_API_URL
Value: https://yourproject-production.up.railway.app
```

(Replace with your actual Railway URL)

#### Step 3: Build Settings
- Build Command: (leave empty or `npm install`)
- Output Directory: `frontend`
- Install Command: (leave empty)

#### Step 4: Deploy
Click "Deploy" - Vercel akan deploy frontend

---

## 🔗 Update Frontend API URL

Edit `frontend/app.js` to use environment variable:

```javascript
// At the top of file
const API_BASE_URL = process.env.VITE_API_URL || 'http://127.0.0.1:8000';

// In uploadSection event listener
const formData = new FormData();
formData.append('file', file);

const response = await fetch(`${API_BASE_URL}/detect`, {
    method: 'POST',
    body: formData
});
```

---

## 📝 Step-by-Step Deployment

### Backend to Railway

```bash
# 1. Push to GitHub (already done)
cd "c:\Users\rayha\Documents\Detector Rail Kereta Api"
git add .
git commit -m "Add Railway deployment config"
git push origin main

# 2. Go to https://railway.app/dashboard
# 3. Click "New Project"
# 4. Select "Deploy from GitHub repo"
# 5. Choose your repository
# 6. Railway auto-deploys!
# 7. Wait for deployment (usually 2-5 minutes)
# 8. Copy the deployment URL
```

### Frontend to Vercel

```bash
# 1. Go to https://vercel.com/new
# 2. Import your GitHub repo
# 3. Framework: Other
# 4. Root Directory: frontend
# 5. Add env var: VITE_API_URL = <Railway-URL>
# 6. Click Deploy
# 7. Wait for deployment
# 8. Get your frontend URL (e.g., yourname.vercel.app)
```

---

## ✅ Verification Checklist

### Railway Backend
- [ ] Deployment shows "Deployed"
- [ ] View logs - no errors
- [ ] Test API: `curl https://your-railway-url/docs`
- [ ] Should see FastAPI Swagger UI

### Vercel Frontend
- [ ] Deployment shows "Ready"
- [ ] Visit yourname.vercel.app
- [ ] Upload image works
- [ ] Detections displayed correctly
- [ ] API calls go to Railway backend

---

## 🔧 Troubleshooting

### Backend Issues

**Error: "No module named 'fastapi'"**
- Railway needs to install dependencies from requirements.txt
- Check Railway knows it's Python project
- Verify Procfile is correct

**Error: "Model not found"**
- Ensure `backend/models/best.pt` exists
- Railway should have cloned entire repo

**Error: "Port already in use"**
- Procfile should use `$PORT` variable
- Railway manages port assignment

### Frontend Issues

**API calls failing**
- Check VITE_API_URL environment variable in Vercel
- Ensure Railway backend is running
- Check CORS settings in backend (should be enabled)

**Build fails on Vercel**
- Make sure `frontend/` folder has index.html
- Remove Node.js dependencies from frontend if not needed
- Check .vercelignore excludes unnecessary files

---

## 📊 Monitor Deployments

### Railway
- Dashboard: https://railway.app/dashboard
- View logs, environment, metrics
- Redeploy: Push to GitHub or manual trigger

### Vercel
- Dashboard: https://vercel.com/dashboard
- View deployments, analytics
- Preview URLs for PRs

---

## 🚨 Important Notes

1. **Model Size**: best.pt (13.76 MB) will be included
   - Railway: ✅ No size limit for repo
   - Vercel: ⚠️ Might hit size limits - if issue, use Git LFS

2. **First Request Delay**: Model loading takes ~30 seconds
   - First API call will be slow (model loads)
   - Subsequent calls ~180ms

3. **CORS**: Backend has CORS enabled for any origin
   - Production: Consider restricting to Vercel domain

4. **Secrets**: No secrets in repo (good practice)
   - Environment variables via platform

---

## 🎯 Next Steps

1. **Push deployment configs:**
```bash
cd "c:\Users\rayha\Documents\Detector Rail Kereta Api"
git add Procfile vercel.json .vercelignore
git commit -m "Add Railway and Vercel deployment configs"
git push origin main
```

2. **Deploy to Railway:**
   - Go to https://railway.app
   - New Project → GitHub repo
   - Auto-deploy begins

3. **Deploy to Vercel:**
   - Go to https://vercel.com
   - New Project → GitHub repo
   - Add environment variables
   - Deploy

4. **Update frontend app.js:**
   - Replace API URL with Vercel environment variable
   - Push changes
   - Vercel auto-redeploys

---

## 📱 Final URLs

After deployment you'll have:

- **Backend (Railway):** `https://your-railway-project.up.railway.app`
- **Frontend (Vercel):** `https://your-name.vercel.app`

Share frontend URL with users! 🎉

---

## 🆘 Support

- Railway Docs: https://docs.railway.app/
- Vercel Docs: https://vercel.com/docs
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- GitHub Webhooks: Auto-deploy on push
