# 🔧 Fix Netlify Python Detection Issue

Netlify is trying to install Python dependencies even though this is a static site. Here's how to fix it:

## Problem
Netlify automatically detects `requirements.txt` and tries to install Python packages, which fails because:
1. This is a static frontend (no Python needed)
2. Some packages like `pyarrow` require compilation and fail on Netlify

## Solution: Configure Netlify Dashboard

Since `.netlifyignore` might not prevent auto-detection, you need to configure Netlify dashboard:

### Step 1: Go to Netlify Dashboard
1. Log in to https://app.netlify.com
2. Select your site
3. Go to **Site settings** → **Build & deploy** → **Build settings**

### Step 2: Update Build Settings
1. **Build command**: Leave **EMPTY** or set to: `echo "Static site"`
2. **Publish directory**: Set to `.` (dot/period)
3. **Base directory**: Leave **EMPTY**

### Step 3: Clear Build Cache
1. Go to **Deploys** tab
2. Click **"Trigger deploy"** → **"Clear cache and deploy site"**
3. This will force a fresh build without cached Python detection

### Step 4: Alternative - Use Environment Variable
If the above doesn't work, add an environment variable:
1. Go to **Site settings** → **Environment variables**
2. Add new variable:
   - **Key**: `SKIP_PYTHON_INSTALL`
   - **Value**: `true`
3. Redeploy

## Alternative Solution: Move Backend Files

If Netlify keeps detecting Python, you can:
1. Move backend files to a `backend/` folder
2. Keep only frontend files in root
3. Update your repository structure

## Quick Fix Command

After updating settings, trigger a new deploy:
- Go to **Deploys** → **Trigger deploy** → **Deploy site**

---

**The `.netlifyignore` file should work, but Netlify's auto-detection might run before it's processed. The dashboard settings override this.**

