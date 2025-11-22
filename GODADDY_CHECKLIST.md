# ✅ GoDaddy Deployment Checklist

Use this checklist to ensure everything is set up correctly.

## 📋 Pre-Deployment

- [ ] GoDaddy hosting account active
- [ ] Domain name configured
- [ ] cPanel access available
- [ ] FTP credentials ready (optional, for FileZilla)

## 📤 Frontend Upload

- [ ] Logged into GoDaddy cPanel
- [ ] Opened File Manager
- [ ] Navigated to `public_html` folder
- [ ] Uploaded `index.html`
- [ ] Uploaded `login.html`
- [ ] Uploaded `dashboard.html`
- [ ] Uploaded `budget-optimizer.html`
- [ ] Uploaded `investment-guide.html`
- [ ] Uploaded `about.html`
- [ ] Uploaded `blog.html`
- [ ] Uploaded `help.html`
- [ ] Uploaded `styles.css`
- [ ] Uploaded `script.js`
- [ ] Uploaded `manifest.json`
- [ ] Uploaded `service-worker.js`
- [ ] Uploaded `.htaccess` file

## 🔧 Backend Setup

- [ ] Created Render account (or have GoDaddy VPS)
- [ ] Deployed backend to Render
- [ ] Got Render backend URL
- [ ] Updated `.htaccess` with Render URL
- [ ] Set environment variables on Render:
  - [ ] `PYTHON_VERSION=3.11.9`
  - [ ] `JWT_SECRET=<random-string>`

## ⚙️ Configuration

- [ ] `.htaccess` file exists in `public_html`
- [ ] `.htaccess` has correct Render URL (not `YOUR-RENDER-URL`)
- [ ] File permissions correct (644 for files, 755 for folders)
- [ ] No syntax errors in `.htaccess`

## 🔒 Security & SSL

- [ ] SSL certificate installed (check SSL/TLS Status in cPanel)
- [ ] HTTPS redirect working
- [ ] Security headers configured in `.htaccess`

## ✅ Testing

- [ ] Homepage loads: `https://yourdomain.com`
- [ ] Navigation works
- [ ] Login page loads
- [ ] Can create account
- [ ] Can log in
- [ ] Dashboard loads
- [ ] Budget Optimizer works
- [ ] Investment Guide works
- [ ] No console errors (F12 → Console)
- [ ] API calls working (F12 → Network tab)

## 📊 Post-Deployment

- [ ] Analytics working (Plausible)
- [ ] Error logging working
- [ ] Mobile responsive (test on phone)
- [ ] All pages accessible
- [ ] Forms submit correctly

## 🎯 Final Verification

- [ ] Site accessible via domain name
- [ ] SSL certificate active (green lock icon)
- [ ] All features functional
- [ ] No broken links
- [ ] Images loading correctly
- [ ] CSS styling applied

---

## 🐛 If Something's Wrong

1. **Check File Locations**: All files must be in `public_html` root
2. **Check .htaccess**: Must have correct Render URL
3. **Check Backend**: Verify Render service is running
4. **Check Browser Console**: Look for JavaScript errors
5. **Check File Permissions**: Should be 644/755
6. **Clear Cache**: Browser cache and CDN cache

---

## 📞 Need Help?

- **GoDaddy Support**: Live chat in dashboard
- **Render Support**: Check Render logs
- **Documentation**: See `GODADDY_DEPLOYMENT.md`

---

**Once all items are checked, your site is live! 🎉**

