# 🚀 Deployment Guide - Ghar Ka Guide

This guide will help you deploy your website to production in **under 30 minutes**.

## 📋 Prerequisites

1. **GitHub Account** (free) - [Sign up here](https://github.com)
2. **Render Account** (free) - [Sign up here](https://render.com)
3. **Netlify Account** (free) - [Sign up here](https://netlify.com)

---

## 🎯 Step 1: Prepare Your Code

### 1.1 Initialize Git Repository

```bash
cd c:\Users\jayaaditya-s\MyWebsite
git init
git add .
git commit -m "Initial commit - Ghar Ka Guide website"
```

### 1.2 Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `ghar-ka-guide` (or any name you prefer)
3. **Don't** initialize with README, .gitignore, or license
4. Copy the repository URL (e.g., `https://github.com/yourusername/ghar-ka-guide.git`)

### 1.3 Push to GitHub

```bash
git remote add origin https://github.com/yourusername/ghar-ka-guide.git
git branch -M main
git push -u origin main
```

---

## 🔧 Step 2: Deploy Backend to Render

### 2.1 Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository (`ghar-ka-guide`)

### 2.2 Configure Backend Service

**Settings:**
- **Name**: `ghar-ka-guide-backend` (or any name)
- **Region**: Choose closest to your users (e.g., `Singapore` for India)
- **Branch**: `main`
- **Root Directory**: Leave empty (or `backend` if you move files)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 2.3 Environment Variables

Click **"Environment"** tab and add:

```
PYTHON_VERSION=3.11.9
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
```

**Important**: 
- Generate a strong JWT_SECRET: Use a random string generator or `openssl rand -hex 32`
- If you're not using Ollama, you can leave those variables empty

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for first deployment
3. **Copy your service URL** (e.g., `https://ghar-ka-guide-backend.onrender.com`)

---

## 🌐 Step 3: Deploy Frontend to Netlify

### 3.1 Update Configuration Files

**Update `_redirects` file:**
Replace `YOUR-RENDER-SUBDOMAIN.onrender.com` with your actual Render URL:

```
/api/*  https://ghar-ka-guide-backend.onrender.com/api/:splat  200
```

**Update `netlify.toml` file:**
Replace `YOUR-RENDER-SUBDOMAIN.onrender.com` with your actual Render URL in the CSP header.

### 3.2 Deploy via GitHub

1. Go to [Netlify](https://app.netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **"GitHub"** and authorize Netlify
4. Select your repository (`ghar-ka-guide`)

### 3.3 Configure Build Settings

**Settings:**
- **Base directory**: Leave empty
- **Build command**: Leave empty (static site)
- **Publish directory**: `.` (root directory)

### 3.4 Deploy

1. Click **"Deploy site"**
2. Wait 2-3 minutes for deployment
3. **Copy your site URL** (e.g., `https://amazing-site-12345.netlify.app`)

---

## ✅ Step 4: Final Configuration

### 4.1 Update Frontend API Calls

Your frontend already uses relative paths (`/api/*`), so Netlify redirects will handle this automatically. No changes needed!

### 4.2 Test Your Deployment

1. Visit your Netlify URL
2. Try logging in
3. Test the dashboard
4. Test the budget optimizer
5. Test the investment guide

### 4.3 Custom Domain (Optional)

**Netlify:**
1. Go to **"Domain settings"** in your Netlify site
2. Click **"Add custom domain"**
3. Enter your domain (e.g., `gharkaguide.com`)
4. Follow DNS configuration instructions

**Render:**
1. Go to your Render service settings
2. Add custom domain if needed
3. Update CORS settings if using custom domain

---

## 🔒 Step 5: Security Checklist

- [x] JWT_SECRET is set in Render environment variables
- [x] CORS is configured in `app.py`
- [x] Security headers are set in `netlify.toml`
- [x] HTTPS is enabled (automatic on Netlify/Render)
- [x] `.gitignore` excludes sensitive files

---

## 📊 Step 6: Monitor Your Site

### Analytics
- Plausible analytics is already integrated
- Visit [Plausible](https://plausible.io) to view stats (if you set up an account)

### Error Logging
- Errors are logged to `errors.json` on Render
- Access via Render logs or download the file

### Backend Logs
- View logs in Render dashboard → Your service → Logs

---

## 🐛 Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify `requirements.txt` has all dependencies
- Ensure `Procfile` exists and is correct

### Frontend can't connect to backend
- Verify `_redirects` file has correct Render URL
- Check CORS settings in `app.py`
- Test backend URL directly: `https://your-backend.onrender.com/`

### 404 errors on frontend
- Ensure `netlify.toml` is in root directory
- Check that `_redirects` file is in root (not in a subdirectory)

### Authentication not working
- Verify JWT_SECRET is set in Render
- Check browser console for errors
- Ensure API endpoints are accessible

---

## 🎉 You're Live!

Your website is now deployed and accessible to the world!

**Frontend**: `https://your-site.netlify.app`  
**Backend**: `https://your-backend.onrender.com`

---

## 📝 Quick Reference

### Update Your Site

```bash
# Make changes to your files
git add .
git commit -m "Your update message"
git push origin main
```

Both Netlify and Render will automatically redeploy!

### Local Development

```bash
# Backend
python app.py

# Frontend
# Just open index.html in browser or use:
python -m http.server 8000
```

---

## 💡 Pro Tips

1. **Free Tier Limits**:
   - Render: Free tier spins down after 15 min inactivity (first request may be slow)
   - Netlify: 100GB bandwidth/month (usually plenty)

2. **Upgrade Options**:
   - Render: $7/month for always-on service
   - Netlify: Pro plan for more features

3. **Database** (Future):
   - Consider Render PostgreSQL for production
   - Or use MongoDB Atlas (free tier)

4. **CDN**:
   - Netlify automatically provides CDN
   - Images should be optimized before upload

---

**Need Help?** Check the logs in Render and Netlify dashboards for detailed error messages.

