### ⚙️ Features
- Extracts Txt from **AppxV2 & AppxV3** platforms
- Supports **Khan GS**, **ClassPlus**, and **PW (PhysicsWallah)**
- Token-based and login-based extraction supported
- Clean UI with Telegram buttons (use `/start` to begin)
- Admin-only premium controls available in `modules/`

---

### 🚀 How to Use
Just send `/start` — all features are handled via buttons.
### 🔑 Required Environment Variables (.env)
You need to set the following variables for the bot to run. These are read using `os.environ.get()` in the code.

```env
API_ID=123456               # Get from https://my.telegram.org
API_HASH=your_api_hash     # Get from https://my.telegram.org
BOT_TOKEN=your_bot_token   # Get from https://t.me/BotFather
OWNER_ID=123456789         # Your Telegram user ID
SUDO_USERS=123456789 987654321  # Space-separated admin user IDs
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/...  # MongoDB connection URI
CHANNEL_ID=-100xxxxxxxxxx  # Telegram channel ID with -100 prefix
```

> **Where to get these?**  
• `API_ID` & `API_HASH` → [my.telegram.org](https://my.telegram.org) → API Development Tools  
• `BOT_TOKEN` → [@BotFather](https://t.me/BotFather)  
• `OWNER_ID`, `SUDO_USERS` → Get your Telegram ID from [@userinfobot](https://t.me/userinfobot)  
• `CHANNEL_ID` → Right-click channel > Copy ID (if bot is admin)  
• `MONGO_URL` → From your MongoDB Atlas project dashboard

---
### ☁️ Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kratik00/EXTRACTOR-TXT)

### ☁️ Deploy to Heroku (Manual)
```bash
1. Fork this repo
2. Create a new Heroku app
3. Set buildpacks: heroku/python
4. Add env variables: API_ID, API_HASH, BOT_TOKEN, etc.
5. Deploy your app and scale worker to 1
```

---

