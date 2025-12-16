# 📤 GitHub Upload Guide

## Quick Steps

### 1. Prepare Local Repository

```bash
cd "c:\Users\rayha\Documents\Detector Rail Kereta Api"

# Initialize git
git init

# Configure git
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Railway Track Inspection System - AI-powered fault detection"
```

### 2. Create Repository on GitHub

1. Go to https://github.com/new
2. Enter details:
   - **Repository name:** `railway-track-inspection`
   - **Description:** AI-Powered Railway Track Fault Detection System
   - **Privacy:** Public (for visibility) or Private (for security)
   - **Add .gitignore:** Already configured ✓
   - **Add README:** Already included ✓

3. Click "Create repository"

### 3. Connect Local to Remote

After creating repo on GitHub, you'll see these commands:

```bash
# If you created NEW empty repository:
git remote add origin https://github.com/YOUR_USERNAME/railway-track-inspection.git
git branch -M main
git push -u origin main

# If you need to push to existing:
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username!**

---

## Complete Example

```bash
# 1. Navigate to project
cd "c:\Users\rayha\Documents\Detector Rail Kereta Api"

# 2. Initialize and commit (if not done)
git init
git config user.email "john@example.com"
git config user.name "John Doe"
git add .
git commit -m "Initial commit: Railway Track Inspection System"

# 3. Add remote (replace with your username)
git remote add origin https://github.com/johndoe/railway-track-inspection.git

# 4. Push to GitHub
git branch -M main
git push -u origin main
```

---

## What Gets Uploaded

✅ **Included:**
- Backend API code (main.py)
- Frontend UI (HTML/CSS/JS)
- Trained model (best.pt)
- Configuration files
- Documentation (README.md, DEPLOYMENT.md, etc.)
- Docker support

❌ **Excluded (via .gitignore):**
- Dataset images (too large)
- `__pycache__` directories
- Virtual environments
- Log files
- Temporary test files

---

## After Upload

### Make it Public-Ready

1. **Add to GitHub Topics:**
   - Repository Settings → About → Topics
   - Add: `yolov5`, `object-detection`, `railway`, `fastapi`, `python`

2. **Enable GitHub Pages** (Optional):
   - Settings → Pages
   - Source: main branch / docs folder

3. **Add Badges to README:**
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.10+-blue)
   ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)
   ![YOLOv5](https://img.shields.io/badge/YOLOv5-v7.0-orange)
   ![License](https://img.shields.io/badge/license-MIT-green)
   ```

4. **Create Release:**
   - Go to Releases
   - Create new release (v1.0.0)
   - Add description
   - Attach deployment package

---

## Automated Setup (Windows)

Run the provided script:
```bash
upload-github.bat
```

This will:
1. Initialize git repo
2. Add all files
3. Create initial commit
4. Display next steps

---

## Troubleshooting

### Git not recognized
```bash
# Check if git is installed
git --version

# If not, install from: https://git-scm.com/
```

### Authentication error
```bash
# For HTTPS (recommended for Windows):
git config --global credential.helper wincred

# Or use Personal Access Token:
# https://github.com/settings/tokens
```

### Need to change remote
```bash
# Check current remote
git remote -v

# Change remote
git remote set-url origin https://github.com/YOUR_USERNAME/railway-track-inspection.git
```

### Large file error
```bash
# If model file is too large for GitHub
# Install Git LFS: https://git-lfs.github.com/

# Track large files
git lfs track "*.pt"
git add .gitattributes

# Then push as normal
git push -u origin main
```

---

## Deployment from GitHub

### Automatic Deployment (Railway.app)

1. Install Railway CLI
2. Connect GitHub repository
3. Railway auto-deploys on push

```bash
# Login to Railway
railway login

# Create project
railway init

# Deploy
railway up
```

### Manual Deployment

Clone from GitHub and deploy:
```bash
git clone https://github.com/YOUR_USERNAME/railway-track-inspection.git
cd railway-track-inspection
docker-compose up -d
```

---

## GitHub Actions (CI/CD) - Optional

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      - name: Lint with flake8
        run: |
          flake8 backend/main.py --max-line-length=100
```

---

## Resources

- **Git Documentation:** https://git-scm.com/doc
- **GitHub Guides:** https://guides.github.com/
- **Git LFS:** https://git-lfs.github.com/
- **Railway.app:** https://railway.app/
- **GitHub Actions:** https://docs.github.com/en/actions

---

**Ready to share your project with the world! 🚀**
