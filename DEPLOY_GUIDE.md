# 🚀 Quick Deploy to Streamlit Cloud (5 Minutes)

## ✅ What You Need

1. **GitHub account** (free) - [github.com](https://github.com)
2. **Streamlit account** (free) - [streamlit.io/cloud](https://streamlit.io/cloud)
3. **Groq API key** (free) - [console.groq.com](https://console.groq.com)

---

## 🎯 Option 1: Deploy from GitHub (Recommended)

### Step 1: Get Your Groq API Key (1 minute)

1. Go to https://console.groq.com
2. Sign up (free, no credit card!)
3. Click **"API Keys"** → **"Create API Key"**
4. Copy your key (starts with `gsk_...`)

### Step 2: Push Code to GitHub (2 minutes)

```bash
# Navigate to your project folder
cd streamlit-deploy

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/contextiq.git
git push -u origin main
```

**Don't have git?** 
- Go to [github.com/new](https://github.com/new)
- Create new repo named "contextiq"
- Upload all files from web interface

### Step 3: Deploy on Streamlit (2 minutes)

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Connect to GitHub (if first time)
4. Fill in:
   - **Repository**: `YOUR_USERNAME/contextiq`
   - **Branch**: `main`
   - **Main file**: `app.py`
5. Click **"Advanced settings"**
6. In **Secrets**, paste:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_api_key_here"
   ```
7. Click **"Deploy!"**
8. Wait 2-3 minutes ☕
9. **Done!** Your app is live! 🎉

---

## 🎯 Option 2: Deploy Without Git (Direct Upload)

### For GitHub Desktop Users:

1. Open GitHub Desktop
2. File → Add Local Repository → Select your folder
3. Commit changes
4. Publish repository
5. Follow Step 3 above

### For Non-Git Users:

1. Zip your `streamlit-deploy` folder
2. Go to [github.com/new](https://github.com/new)
3. Create repo, then upload zip
4. Extract files in GitHub
5. Follow Step 3 above

---

## 🔧 Adding Secrets After Deployment

If you forgot to add secrets during deployment:

1. Go to your app dashboard: https://share.streamlit.io
2. Click on your app
3. Click **"Settings"** (⚙️ icon)
4. Click **"Secrets"** in sidebar
5. Paste:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
6. Click **"Save"**
7. App automatically restarts! ✅

---

## 📱 Share Your App

Your app URL will be:
```
https://YOUR_USERNAME-contextiq-app-RANDOM.streamlit.app
```

**Pro tip**: You can customize the URL in settings!

---

## 🎨 Customize After Deploy

Want to make changes?

1. Edit files locally
2. Test: `streamlit run app.py`
3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Updated feature"
   git push
   ```
4. Streamlit auto-updates! ⚡

---

## ✅ Deployment Checklist

Before deploying, make sure:

- [ ] All files in folder (app.py, llm_engine.py, requirements.txt)
- [ ] Got your Groq API key
- [ ] Created GitHub account
- [ ] Created Streamlit account
- [ ] Code pushed to GitHub
- [ ] Secrets added in Streamlit

---

## 🆘 Troubleshooting

### "Error: GROQ_API_KEY not found"
→ Add it in Streamlit Settings → Secrets

### "App won't start"
→ Check logs in Streamlit dashboard
→ Verify requirements.txt

### "Repository not found"
→ Make sure repo is public
→ Reconnect GitHub in Streamlit

### "Build failed"
→ Check all files are pushed
→ Verify requirements.txt syntax

---

## 💡 Tips

✅ **Use descriptive repo name** (e.g., "contextiq-ai-assistant")  
✅ **Make repo public** for free hosting  
✅ **Keep secrets.toml in .gitignore** (it's already there)  
✅ **Test locally first** with `streamlit run app.py`  
✅ **Check Streamlit logs** if issues occur  

---

## 🎉 Success!

Your AI assistant is now live and accessible to anyone!

**Next steps:**
- Share your app URL with friends
- Customize the UI in `app.py`
- Add new features
- Join Streamlit community

---

## 📊 Streamlit Cloud Features

**Free Tier Includes:**
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Auto-deploys from GitHub
- ✅ HTTPS & custom domains
- ✅ 99.9% uptime
- ✅ Community support

**Total Cost: $0** 🎉

---

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **Deploy Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Groq Docs**: https://console.groq.com/docs
- **Community**: https://discuss.streamlit.io

---

**Happy Deploying!** 🚀✨
