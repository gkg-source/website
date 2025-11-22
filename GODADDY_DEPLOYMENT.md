# 🚀 GoDaddy Deployment Guide

This guide will help you deploy your Ghar Ka Guide website to GoDaddy hosting.

## 📋 Prerequisites

1. **GoDaddy Account** with hosting plan
2. **Domain name** (if not already purchased)
3. **FTP Client** (FileZilla, WinSCP, or GoDaddy's File Manager)
4. **Python Support** (check if your GoDaddy plan supports Python/Flask)

---

## 🔍 Step 1: Check Your GoDaddy Hosting Plan

GoDaddy offers different hosting types:

### Option A: Shared Hosting (Linux)
- ✅ Supports static HTML/CSS/JS files
- ⚠️ May or may not support Python/Flask
- ✅ Usually includes cPanel
- 💰 Most affordable option

### Option B: VPS/Dedicated Server
- ✅ Full control, supports Python/Flask
- ✅ Can run backend on same server
- 💰 More expensive

### Option C: Hybrid Approach (Recommended)
- **Frontend**: GoDaddy shared hosting (static files)
- **Backend**: Keep on Render (free) or deploy to GoDaddy VPS
- ✅ Best of both worlds

---

## 🎯 Recommended Approach: Hybrid Deployment

**Why?** GoDaddy shared hosting often doesn't support Python/Flask well. This approach:
- Hosts frontend on GoDaddy (fast, reliable)
- Keeps backend on Render (free, reliable)
- Works seamlessly together

---

## 📤 Step 2: Deploy Frontend to GoDaddy

### 2.1 Access Your GoDaddy Account

1. Log in to [GoDaddy](https://www.godaddy.com)
2. Go to **My Products** → **Web Hosting**
3. Click **Manage** on your hosting plan
4. Open **cPanel** or **File Manager**

### 2.2 Upload Frontend Files

**Via File Manager (Easiest):**
1. In cPanel, click **File Manager**
2. Navigate to `public_html` folder (or `htdocs` for some plans)
3. Delete default files (index.html, etc.) if needed
4. Upload all your frontend files:
   - `index.html`
   - `login.html`
   - `dashboard.html`
   - `budget-optimizer.html`
   - `investment-guide.html`
   - `about.html`
   - `blog.html`
   - `help.html`
   - `styles.css`
   - `script.js`
   - `manifest.json`
   - `service-worker.js`
   - `_redirects` (rename to `.htaccess` - see below)
   - `netlify.toml` (not needed for GoDaddy)

**Via FTP:**
1. Get FTP credentials from GoDaddy cPanel
2. Use FileZilla or similar FTP client
3. Connect to your server
4. Upload files to `public_html` directory

### 2.3 Create .htaccess File

GoDaddy uses Apache, so we need `.htaccess` instead of `_redirects`.

Create a file named `.htaccess` in your `public_html` folder with:

```apache
# Enable Rewrite Engine
RewriteEngine On

# API Proxy to Backend (if using Render)
RewriteCond %{REQUEST_URI} ^/api/(.*)$
RewriteRule ^api/(.*)$ https://YOUR-RENDER-URL.onrender.com/api/$1 [P,L]

# Security Headers
<IfModule mod_headers.c>
    Header set X-Frame-Options "DENY"
    Header set X-Content-Type-Options "nosniff"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
    Header set Content-Security-Policy "default-src 'self' https://YOUR-RENDER-URL.onrender.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com"
</IfModule>

# Enable CORS (if needed)
<IfModule mod_headers.c>
    Header set Access-Control-Allow-Origin "*"
    Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
    Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>

# Cache Control
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Gzip Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>
```

**Important:** Replace `YOUR-RENDER-URL.onrender.com` with your actual Render backend URL.

### 2.4 Test Frontend

1. Visit your domain: `https://yourdomain.com`
2. Check if homepage loads
3. Test navigation
4. Check browser console for errors

---

## 🔧 Step 3: Deploy Backend

### Option A: Keep Backend on Render (Recommended)

**Why?** GoDaddy shared hosting often doesn't support Python/Flask well.

1. Follow the Render deployment from `DEPLOYMENT.md`
2. Get your Render backend URL
3. Update `.htaccess` with your Render URL (done in Step 2.3)
4. Done! Your frontend on GoDaddy will proxy API calls to Render.

### Option B: Deploy Backend to GoDaddy VPS

If you have GoDaddy VPS or want to host everything on GoDaddy:

#### 3.1 Set Up Python Environment

1. SSH into your VPS
2. Install Python 3.11:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### 3.2 Create Application Directory

```bash
cd /var/www
sudo mkdir ghar-ka-guide-api
sudo chown $USER:$USER ghar-ka-guide-api
cd ghar-ka-guide-api
```

#### 3.3 Upload Backend Files

Upload via FTP or SCP:
- `app.py`
- `requirements.txt`
- All Python modules (if you have them)

#### 3.4 Set Up Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3.5 Install Gunicorn

```bash
pip install gunicorn
```

#### 3.6 Create Systemd Service

Create `/etc/systemd/system/ghar-ka-guide-api.service`:

```ini
[Unit]
Description=Ghar Ka Guide API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ghar-ka-guide-api
Environment="PATH=/var/www/ghar-ka-guide-api/venv/bin"
ExecStart=/var/www/ghar-ka-guide-api/venv/bin/gunicorn --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

#### 3.7 Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable ghar-ka-guide-api
sudo systemctl start ghar-ka-guide-api
sudo systemctl status ghar-ka-guide-api
```

#### 3.8 Configure Nginx/Apache Reverse Proxy

Update your `.htaccess` or Apache config to proxy `/api/*` to `http://127.0.0.1:5000`

---

## 🔄 Step 4: Update Frontend Configuration

### 4.1 Update API Base URL (if needed)

If your backend is on the same domain, you can use relative paths (already configured).

If backend is on Render, the `.htaccess` proxy will handle it automatically.

### 4.2 Test API Connection

1. Open browser console
2. Visit your site
3. Try logging in
4. Check Network tab for API calls
5. Verify they're going to the right backend

---

## 🔒 Step 5: SSL Certificate

GoDaddy usually provides free SSL certificates:

1. In cPanel, find **SSL/TLS Status**
2. Install SSL certificate for your domain
3. Force HTTPS redirect in `.htaccess`:

```apache
# Force HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

---

## 📁 Step 6: File Structure on GoDaddy

Your `public_html` folder should look like:

```
public_html/
├── index.html
├── login.html
├── dashboard.html
├── budget-optimizer.html
├── investment-guide.html
├── about.html
├── blog.html
├── help.html
├── styles.css
├── script.js
├── manifest.json
├── service-worker.js
├── .htaccess
└── icons/ (if you have PWA icons)
    ├── icon-192.png
    └── icon-512.png
```

---

## ✅ Step 7: Final Checklist

- [ ] All HTML files uploaded to `public_html`
- [ ] CSS and JS files uploaded
- [ ] `.htaccess` file created with correct backend URL
- [ ] Backend deployed (Render or GoDaddy VPS)
- [ ] SSL certificate installed
- [ ] Domain points to GoDaddy hosting
- [ ] Test homepage loads
- [ ] Test login/signup
- [ ] Test API calls work
- [ ] Check browser console for errors

---

## 🐛 Troubleshooting

### Frontend not loading
- Check file permissions (should be 644 for files, 755 for folders)
- Verify files are in `public_html` (not a subfolder)
- Clear browser cache
- Check `.htaccess` syntax

### API calls failing
- Verify `.htaccess` proxy rule is correct
- Check backend URL is accessible
- Verify CORS settings in backend
- Check browser console for specific errors

### 500 Internal Server Error
- Check `.htaccess` syntax
- Verify mod_rewrite is enabled (contact GoDaddy support)
- Check error logs in cPanel

### SSL not working
- Wait 24-48 hours for SSL to propagate
- Clear browser cache
- Try incognito mode
- Contact GoDaddy support

---

## 💡 Pro Tips

1. **Backup First**: Always backup your files before making changes
2. **Test Locally**: Test `.htaccess` changes locally if possible
3. **Monitor Logs**: Check error logs in cPanel regularly
4. **Keep Backend on Render**: Easier to manage and update
5. **Use CDN**: Consider Cloudflare for better performance

---

## 📞 GoDaddy Support

If you encounter issues:
- **Live Chat**: Available in GoDaddy dashboard
- **Phone**: 1-480-505-8877 (US)
- **Help Center**: https://www.godaddy.com/help

---

## 🎉 You're Live!

Once everything is set up, your website will be accessible at:
**https://yourdomain.com**

---

## 🔄 Updating Your Site

### Via File Manager:
1. Log in to GoDaddy cPanel
2. Open File Manager
3. Navigate to `public_html`
4. Upload new files (overwrite old ones)
5. Clear browser cache

### Via FTP:
1. Connect via FTP client
2. Upload changed files
3. Files update immediately

---

**Need help?** Check GoDaddy's documentation or contact their support team.

