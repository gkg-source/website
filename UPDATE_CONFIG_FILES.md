# 📝 How to Update Config Files

This guide shows you exactly how to update the configuration files with your Render backend URL.

## 🎯 Which Files to Update?

**If deploying to Netlify:**
- Update `_redirects`
- Update `netlify.toml`

**If deploying to GoDaddy:**
- Update `.htaccess` (ignore `_redirects` and `netlify.toml`)

---

## Option 1: Deploying to Netlify

### Step 1: Get Your Render Backend URL

1. Go to https://dashboard.render.com
2. Click on your backend service
3. Copy the URL (e.g., `https://ghar-ka-guide-backend.onrender.com`)

### Step 2: Update `_redirects` File

1. Open `_redirects` file in your editor
2. Find this line:
   ```
   /api/*  https://YOUR-RENDER-SUBDOMAIN.onrender.com/api/:splat  200
   ```
3. Replace `YOUR-RENDER-SUBDOMAIN.onrender.com` with your actual Render URL
4. Example (if your Render URL is `ghar-ka-guide-backend.onrender.com`):
   ```
   /api/*  https://ghar-ka-guide-backend.onrender.com/api/:splat  200
   ```
5. Save the file

### Step 3: Update `netlify.toml` File

1. Open `netlify.toml` file in your editor
2. Find line 3 (the `to` field):
   ```
   to = "https://YOUR-RENDER-SUBDOMAIN.onrender.com/api/:splat"
   ```
3. Replace `YOUR-RENDER-SUBDOMAIN.onrender.com` with your actual Render URL
4. Example:
   ```
   to = "https://ghar-ka-guide-backend.onrender.com/api/:splat"
   ```
5. Find line 13 (the `Content-Security-Policy`):
   ```
   Content-Security-Policy = "... https://YOUR-RENDER-SUBDOMAIN.onrender.com ..."
   ```
6. Replace `YOUR-RENDER-SUBDOMAIN.onrender.com` with your actual Render URL
7. Example:
   ```
   Content-Security-Policy = "... https://ghar-ka-guide-backend.onrender.com ..."
   ```
8. Save the file

### Step 4: Commit and Push to GitHub

Open PowerShell or Command Prompt in your project folder and run:

```bash
# Navigate to your project (if not already there)
cd c:\Users\jayaaditya-s\MyWebsite

# Add the changed files
git add _redirects netlify.toml

# Commit with a message
git commit -m "Update deployment configs with Render URL"

# Push to GitHub
git push
```

**That's it!** Netlify will automatically redeploy with the new configuration.

---

## Option 2: Deploying to GoDaddy

### Step 1: Get Your Render Backend URL

1. Go to https://dashboard.render.com
2. Click on your backend service
3. Copy the URL (e.g., `https://ghar-ka-guide-backend.onrender.com`)

### Step 2: Update `.htaccess` File

1. Open `.htaccess` file in your editor
2. Find lines 9-10 (currently commented out):
   ```
   # RewriteCond %{REQUEST_URI} ^/api/(.*)$
   # RewriteRule ^api/(.*)$ https://YOUR-RENDER-URL.onrender.com/api/$1 [P,L]
   ```
3. **Uncomment** these lines (remove the `#` at the start)
4. Replace `YOUR-RENDER-URL.onrender.com` with your actual Render URL
5. Example:
   ```
   RewriteCond %{REQUEST_URI} ^/api/(.*)$
   RewriteRule ^api/(.*)$ https://ghar-ka-guide-backend.onrender.com/api/$1 [P,L]
   ```
6. Find line 25 (in the `Content-Security-Policy`):
   ```
   Header set Content-Security-Policy "... https://YOUR-RENDER-URL.onrender.com ..."
   ```
7. Replace `YOUR-RENDER-URL.onrender.com` with your actual Render URL
8. Save the file

### Step 3: Upload to GoDaddy

1. Log in to GoDaddy cPanel
2. Open File Manager
3. Navigate to `public_html` folder
4. Upload the updated `.htaccess` file (overwrite the old one)
5. Done!

---

## 📋 Visual Example

### Before (what you see now):
```
/api/*  https://YOUR-RENDER-SUBDOMAIN.onrender.com/api/:splat  200
```

### After (what it should be):
```
/api/*  https://ghar-ka-guide-backend.onrender.com/api/:splat  200
```

**Just replace the placeholder with your actual Render URL!**

---

## 🔍 How to Find Your Render URL

1. Go to https://dashboard.render.com
2. Log in
3. Click on your web service (the one you created for the backend)
4. Look at the top - you'll see something like:
   ```
   https://ghar-ka-guide-backend.onrender.com
   ```
5. Copy that entire URL (without the `/api` part)

---

## ✅ Quick Checklist

- [ ] Got Render backend URL
- [ ] Updated `_redirects` (if using Netlify)
- [ ] Updated `netlify.toml` (if using Netlify)
- [ ] Updated `.htaccess` (if using GoDaddy)
- [ ] Committed and pushed changes (if using Netlify/GitHub)
- [ ] Uploaded `.htaccess` to GoDaddy (if using GoDaddy)

---

## 🐛 Troubleshooting

**Can't find the files?**
- They're in your project root: `c:\Users\jayaaditya-s\MyWebsite\`

**Git commands not working?**
- Make sure you're in the project folder: `cd c:\Users\jayaaditya-s\MyWebsite`
- Make sure Git is installed
- Make sure you've initialized Git: `git init` (if not done already)

**Not sure which platform?**
- **Netlify**: You connected GitHub and deployed via Netlify dashboard
- **GoDaddy**: You uploaded files via cPanel/File Manager

---

**Need help?** Let me know your Render URL and I can help you update the files!

