# 🤖 ContextIQ - AI Assistant for Streamlit Cloud

A powerful, production-ready conversational AI assistant built with **Groq**, **LangChain**, and **Streamlit**. Optimized for Streamlit Cloud deployment.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## ✨ Features

- 🚀 **Ultra-Fast Responses** - Powered by Groq's optimized inference
- 🤖 **Multiple AI Models** - Choose from Llama 3.3 70B, Llama 3.1, Mixtral, Gemma
- 💬 **Smart Conversations** - Maintains context across messages
- 🎨 **Beautiful UI** - Modern, ChatGPT-style interface
- ⚙️ **Customizable** - Adjust temperature, length, and system prompts
- 📊 **Session Stats** - Track your conversation metrics
- 📱 **Mobile-Friendly** - Works perfectly on all devices

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites

1. **GitHub Account** - [Sign up here](https://github.com/join)
2. **Streamlit Account** - [Sign up here](https://streamlit.io/cloud) (use GitHub to sign in)
3. **Groq API Key** - [Get free key here](https://console.groq.com)

### Step-by-Step Deployment (5 minutes)

#### 1. Push Code to GitHub

```bash
# Create a new repository on GitHub (e.g., "contextiq")
# Then push your code:

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/contextiq.git
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Fill in the details:
   - **Repository**: `YOUR_USERNAME/contextiq`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **"Advanced settings"**
5. Add your secret:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. Click **"Deploy"**
7. Wait 2-3 minutes for deployment
8. Your app is live! 🎉

### Alternative: Deploy Without Git

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"** → **"From existing repo"**
3. Choose **"I have an app"**
4. Upload your files directly
5. Add secrets in the dashboard
6. Deploy!

## 🔑 Setting Up Your Groq API Key

### Get Your Free API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up (no credit card needed!)
3. Go to **API Keys** section
4. Click **"Create API Key"**
5. Copy your key (starts with `gsk_...`)

### Add to Streamlit Cloud

**Method 1: During Deployment**
- In "Advanced settings", add:
  ```toml
  GROQ_API_KEY = "gsk_your_actual_key_here"
  ```

**Method 2: After Deployment**
1. Go to your app dashboard
2. Click **"Settings"** → **"Secrets"**
3. Add:
   ```toml
   GROQ_API_KEY = "gsk_your_actual_key_here"
   ```
4. Click **"Save"**
5. App will automatically restart

### For Local Development

Create `.streamlit/secrets.toml` (already included):
```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

**Note**: Never commit this file to Git! (it's already in `.gitignore`)

## 💻 Local Development

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/contextiq.git
cd contextiq

# Install dependencies
pip install -r requirements.txt

# Add your API key to .streamlit/secrets.toml
# Then run the app
streamlit run app.py
```

Your app will open at: http://localhost:8501

## 📁 Project Structure

```
contextiq/
├── app.py                      # Main Streamlit application
├── llm_engine.py              # AI engine with LangChain
├── requirements.txt           # Python dependencies
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.toml          # API keys (template)
├── assets/
│   └── style.css            # Custom styling
├── .gitignore               # Git ignore file
└── README.md               # This file
```

## 🎯 Usage Guide

### Basic Usage

1. Open the app
2. Type your question in the chat input
3. Press Enter
4. Get instant AI responses!

### Customize Settings

Use the sidebar to adjust:
- **AI Model**: Choose based on your needs
- **Temperature**: Control creativity (0.0 = focused, 1.0 = creative)
- **Max Length**: Set response length
- **System Prompt**: Customize AI personality

### Recommended Settings

**For Coding Help:**
- Model: Mixtral 8x7B
- Temperature: 0.2-0.3
- Prompt: "You are an expert programmer..."

**For Creative Writing:**
- Model: Llama 3.3 70B
- Temperature: 0.7-0.8
- Prompt: "You are a creative writing assistant..."

**For General Questions:**
- Model: Llama 3.1 70B
- Temperature: 0.3-0.5
- Default prompt works great

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **LLM Provider**: Groq
- **Models**:
  - Llama 3.3 70B (Most Powerful)
  - Llama 3.1 70B (Balanced)
  - Mixtral 8x7B (Fast & Technical)
  - Gemma 2 9B (Lightweight)
- **Hosting**: Streamlit Cloud (Free!)

## 📊 Performance

- **Response Time**: < 2 seconds average
- **Context Window**: Up to 128K tokens (Llama models)
- **Uptime**: 99.9% (Streamlit Cloud)
- **Concurrent Users**: Scales automatically

## 🔒 Privacy & Security

- ✅ No conversation data stored
- ✅ All chats are session-based
- ✅ API keys secured in Streamlit secrets
- ✅ HTTPS enabled by default
- ✅ No user tracking

## 💰 Costs

### Streamlit Cloud (Free Tier)
- ✅ Free forever
- ✅ 1 GB RAM
- ✅ Unlimited apps
- ✅ Custom domains (paid)

### Groq API (Free Tier)
- ✅ 30 requests/minute
- ✅ 14,400 requests/day
- ✅ No credit card required
- ✅ Generous limits for personal use

**Total Cost**: $0/month for personal use! 🎉

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
**Solution**: Add your API key in Streamlit Cloud Settings → Secrets

### "Rate limit exceeded"
**Solution**: Wait 1 minute or upgrade to Groq paid tier

### App won't start
**Solution**: 
1. Check Streamlit Cloud logs
2. Verify requirements.txt is correct
3. Make sure all files are pushed to GitHub

### Slow responses
**Solution**: 
1. Try a faster model (Gemma 2)
2. Reduce max_tokens
3. Check Groq API status

## 🔄 Updating Your App

1. Make changes to your code locally
2. Test with `streamlit run app.py`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update features"
   git push
   ```
4. Streamlit Cloud auto-deploys! ⚡

## 🎓 Tips for Best Results

1. **Be Specific**: Clear questions → better answers
2. **Provide Context**: Share relevant information
3. **Use Follow-ups**: Build on previous responses
4. **Adjust Temperature**: Match setting to task
5. **Clear History**: Start fresh for new topics

## 📈 Roadmap

- [ ] Streaming responses for better UX
- [ ] File upload support (PDF, TXT)
- [ ] Conversation export/save
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] More LLM providers
- [ ] User authentication
- [ ] Persistent chat history

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📝 License

MIT License - feel free to use for any project!

## 🙏 Acknowledgments

- **Groq** - For ultra-fast LLM inference
- **LangChain** - For excellent LLM framework
- **Streamlit** - For amazing web framework
- **Meta AI** - For Llama models
- **Mistral AI** - For Mixtral model
- **Google** - For Gemma model

## 📧 Support

Need help?
- Check [Streamlit Docs](https://docs.streamlit.io)
- Visit [Groq Docs](https://console.groq.com/docs)
- Open an issue on GitHub
- Join [Streamlit Community](https://discuss.streamlit.io)

---

**Made with Sihab Safin for the AI community**

⭐ Star this repo if you find it useful!

🚀 **Deploy now**: [share.streamlit.io](https://share.streamlit.io)
