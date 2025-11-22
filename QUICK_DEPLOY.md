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

#### Step 4.1: Log in to Netlify
1. Go to **https://app.netlify.com**
2. Click **"Sign up"** (if new) or **"Log in"**
3. Sign up with **GitHub** (recommended - easiest)

#### Step 4.2: Add New Site
1. Click **"Add new site"** button (top right or center)
2. Select **"Import an existing project"**

#### Step 4.3: Connect GitHub
1. Click **"GitHub"** from the Git providers
2. If first time: Click **"Authorize Netlify"** and grant access
3. You'll see a list of your GitHub repositories

#### Step 4.4: Select Your Repository
1. Find and click on your repository (e.g., `ghar-ka-guide`)
2. You can use the search box to find it quickly

#### Step 4.5: Configure Build Settings
**Important:** For a static site, leave these EMPTY:
- **Branch to deploy**: `main` (usually pre-selected)
- **Base directory**: Leave **EMPTY** (your files are in root)
- **Build command**: Leave **EMPTY** (no build needed for static files)
- **Publish directory**: Leave as `.` (root directory)

#### Step 4.6: Deploy
1. Review settings (all should be empty/default)
2. Click **"Deploy site"** button (green, at bottom)
3. Wait 1-3 minutes for deployment
4. Watch the build logs in real-time

#### Step 4.7: Get Your URL
1. Once deployment completes, you'll see:
   - ✅ Status: "Published"
   - **Site URL** (e.g., `https://amazing-site-12345.netlify.app`)
2. **Copy your URL** - Click the copy button or click the URL
3. **Your site is now live!** 🎉

**For detailed instructions, see `NETLIFY_DEPLOYMENT_DETAILED.md`**

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

