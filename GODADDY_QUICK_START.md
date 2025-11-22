# ⚡ GoDaddy Quick Start Guide

Get your website live on GoDaddy in **20 minutes**!

## 🎯 Recommended Setup

**Hybrid Approach** (Easiest & Most Reliable):
- **Frontend**: GoDaddy shared hosting
- **Backend**: Render (free) - keeps it simple!

---

## 📤 Step 1: Upload Frontend to GoDaddy (10 min)

### 1.1 Access GoDaddy cPanel
1. Log in to [GoDaddy](https://www.godaddy.com)
2. Go to **My Products** → **Web Hosting** → **Manage**
3. Click **cPanel** or **File Manager**

### 1.2 Upload Files
1. Navigate to `public_html` folder
2. Delete default files (index.html, etc.) if present
3. Upload ALL these files:
   - ✅ `index.html`
   - ✅ `login.html`
   - ✅ `dashboard.html`
   - ✅ `budget-optimizer.html`
   - ✅ `investment-guide.html`
   - ✅ `about.html`
   - ✅ `blog.html`
   - ✅ `help.html`
   - ✅ `styles.css`
   - ✅ `script.js`
   - ✅ `manifest.json`
   - ✅ `service-worker.js`
   - ✅ `.htaccess` (important!)

**Upload Methods:**
- **File Manager**: Click "Upload" button, select files
- **FTP**: Use FileZilla with credentials from cPanel

### 1.3 Configure .htaccess
1. Open `.htaccess` file in File Manager
2. Find line with `YOUR-RENDER-URL.onrender.com`
3. Replace with your Render backend URL (get it in Step 2)
4. Save file

---

## 🔧 Step 2: Deploy Backend to Render (5 min)

### 2.1 Quick Render Setup
1. Go to https://dashboard.render.com
2. **New +** → **Web Service**
3. Connect GitHub (or use "Public Git repository")
4. Settings:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
5. Environment Variables:
   - `PYTHON_VERSION=3.11.9`
   - `JWT_SECRET=<random-string>`
6. **Create Web Service**
7. Wait 5-10 min → **Copy your Render URL**

### 2.2 Update .htaccess
Go back to GoDaddy File Manager:
1. Edit `.htaccess`
2. Replace `YOUR-RENDER-URL.onrender.com` with your actual Render URL
3. Save

---

## ✅ Step 3: Test & Verify (5 min)

1. Visit your domain: `https://yourdomain.com`
2. Test homepage loads
3. Try login/signup
4. Test dashboard
5. Check browser console (F12) for errors

---

## 🔒 Step 4: Enable SSL (Automatic)

GoDaddy usually auto-installs SSL:
1. In cPanel, find **SSL/TLS Status**
2. If not installed, click **Run AutoSSL**
3. Wait 5-10 minutes
4. Visit `https://yourdomain.com` (should work!)

---

## 📋 File Checklist

Make sure these are in `public_html`:

```
✅ index.html
✅ login.html
✅ dashboard.html
✅ budget-optimizer.html
✅ investment-guide.html
✅ about.html
✅ blog.html
✅ help.html
✅ styles.css
✅ script.js
✅ manifest.json
✅ service-worker.js
✅ .htaccess
```

---

## 🐛 Quick Troubleshooting

**Site not loading?**
- Check files are in `public_html` (not subfolder)
- Verify `.htaccess` exists
- Clear browser cache

**API not working?**
- Check `.htaccess` has correct Render URL
- Verify Render backend is running
- Check browser console (F12) for errors

**SSL not working?**
- Wait 10-15 minutes for propagation
- Try incognito mode
- Contact GoDaddy support

---

## 🎉 Done!

Your site is live at: **https://yourdomain.com**

---

## 🔄 Updating Your Site

**Via File Manager:**
1. Go to cPanel → File Manager
2. Upload new files (overwrite old ones)
3. Done!

**Via FTP:**
1. Connect with FileZilla
2. Upload changed files
3. Files update immediately

---

**Need detailed instructions?** See `GODADDY_DEPLOYMENT.md`

