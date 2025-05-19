<p align="center">
  <a href="https://t.me/spidy-bots">
    <img src="https://img.shields.io/badge/SPIDY-BOTS-303030?style=for-the-badge&logo=telegram&logoColor=white"/>
  </a>
</p>

<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=900&size=30&pause=1000&center=true&vCenter=true&multiline=true&repeat=true&width=500&lines=TXT+EXTRACTOR;Extract+content+from+multiple+edtech+apps;Click+%2Fstart+to+begin"/>
</h1>

---

### ⚙️ Features
- Extracts Txt from **AppxV2 & AppxV3** platforms
- Supports **Khan GS**, **ClassPlus**, and **PW (PhysicsWallah)**
- Token-based and login-based extraction supported
- Clean UI with Telegram buttons (use `/start` to begin)
- Admin-only premium controls available in `modules/`

---

### 🚀 How to Use
Just send `/start` — all features are handled via buttons.

---

### 📸 Screenshots
<p align="center">
  <img src="img/1.jpg" width="45%"/>
  <img src="img/2.jpg" width="45%"/><br>
  <img src="img/3.jpg" width="45%"/>
  <img src="img/4.jpg" width="45%"/><br>
  <img src="img/5.jpg" width="45%"/>
  <img src="img/6.jpg" width="45%"/>
</p>

---
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
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Popeye68/TXT-EXTRACTOR)

### ☁️ Deploy to Heroku (Manual)
```bash
1. Fork this repo
2. Create a new Heroku app
3. Set buildpacks: heroku/python
4. Add env variables: API_ID, API_HASH, BOT_TOKEN, etc.
5. Deploy your app and scale worker to 1
```

---

### 🖥️ VPS Installation
```bash
sudo apt update && sudo apt install git python3-pip -y
git clone https://github.com/Popeye68/TXT-EXTRACTOR
cd TXT-EXTRACTOR
pip3 install -r requirements.txt

# Set your API credentials
export API_ID=123456
export API_HASH=your_api_hash
export BOT_TOKEN=your_bot_token

# Run the bot
python3 bot.py
```

---

### 🔧 Customize Freely
Feel free to **fork this repo**, add your own tweaks, and build your own version.

---

### ⭐ GitHub Buttons

<p align="center">
  <a href="https://github.com/Popeye68/TXT-EXTRACTOR/stargazers">
    <img src="https://img.shields.io/github/stars/Popeye68/TXT-EXTRACTOR.svg?style=for-the-badge&label=Stars&logo=github" />
  </a>
  <a href="https://github.com/Popeye68/TXT-EXTRACTOR/network/members">
    <img src="https://img.shields.io/github/forks/Popeye68/TXT-EXTRACTOR.svg?style=for-the-badge&label=Forks&logo=github" />
  </a>
</p>




---

<p align="center">
  Made with ❤️ by <a href="https://t.me/spidy_bots">Spidy</a>
</p>
