# ⚡ Quick Deployment Checklist

Follow these steps to deploy your website **TODAY**:

## ✅ Pre-Deployment Checklist

- [ ] All files are saved
- [ ] `Procfile` exists (for Render)
- [ ] `requirements.txt` is up to date
- [ ] `.gitignore` is configured
- [ ] `_redirects` file exists (for Netlify)
- [ ] `netlify.toml` exists

## 🚀 Deployment Steps (30 minutes)

### 1. GitHub Setup (5 min)
```bash
git init
git add .
git commit -m "Ready for deployment"
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

### 2. Render Backend (10 min)
1. Go to https://dashboard.render.com
2. New → Web Service
3. Connect GitHub → Select your repo
4. Settings:
   - **Name**: `ghar-ka-guide-api`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
5. Add Environment Variables:
   - `PYTHON_VERSION=3.11.9`
   - `JWT_SECRET=<generate-random-string>`
6. Deploy → **Copy your URL** (e.g., `https://xxx.onrender.com`)

### 3. Update Config Files (2 min)
- Edit `_redirects`: Replace `YOUR-RENDER-SUBDOMAIN` with your Render URL
- Edit `netlify.toml`: Replace `YOUR-RENDER-SUBDOMAIN` in CSP header
- Commit and push:
```bash
git add _redirects netlify.toml
git commit -m "Update deployment configs"
git push
```

### 4. Netlify Frontend (5 min)
1. Go to https://app.netlify.com
2. Add new site → Import from GitHub
3. Select your repo
4. Build settings: Leave empty (static site)
5. Deploy → **Copy your URL**

### 5. Test (5 min)
- Visit your Netlify URL
- Test login/signup
- Test dashboard
- Test tools

## 🎉 Done!

Your site is live! Share your Netlify URL with the world.

## 📝 Important Notes

- **Render free tier**: Spins down after 15 min inactivity (first request may be slow)
- **Update configs**: Remember to update `_redirects` and `netlify.toml` with your Render URL
- **JWT_SECRET**: Generate a strong random string (use `openssl rand -hex 32`)

## 🔄 Updating Your Site

Just push to GitHub:
```bash
git add .
git commit -m "Your changes"
git push
```
Both services auto-deploy!

