# 🤖 Affiliate Bot — 100% Free Automation
### Pinterest + Amazon Affiliate + Blogger | 20 posts/day | ₹0 cost

---

## 📊 Free Tier Usage Summary

| Service         | Free Limit        | We Use      | Status      |
|----------------|-------------------|-------------|-------------|
| Gemini API      | 1,500 req/day     | 60/day      | ✅ Forever  |
| GitHub Actions  | 2,000 mins/month  | ~150 mins   | ✅ Forever  |
| Blogger API     | Unlimited          | 20 posts/day| ✅ Forever  |
| Pinterest API   | Free tier          | 20 pins/day | ✅ Forever  |
| pytrends        | Unlimited          | 20 req/day  | ✅ Forever  |

**Total cost: ₹0/month — Runs indefinitely**

---

## 🔑 Step 1 — Get Your API Keys (All Free)

### A) Gemini API Key (replaces Claude — 100% free)
1. Go to → https://aistudio.google.com/app/apikey
2. Click **"Create API Key"**
3. Copy the key → save as `GEMINI_API_KEY`

### B) Google Blogger API Credentials
1. Go to → https://console.cloud.google.com
2. Create new project → Enable **"Blogger API v3"**
3. Go to **Credentials → Create OAuth 2.0 Client ID**
4. Download JSON credentials
5. Run this once locally to get refresh token:
```bash
pip install google-auth-oauthlib
python setup/get_blogger_token.py
```
6. Copy the output JSON → save as `GOOGLE_CREDENTIALS_JSON`
7. Go to your Blogger dashboard → Settings → find **Blog ID** in the URL
   → save as `BLOGGER_BLOG_ID`

### C) Pinterest Access Token
1. Go to → https://developers.pinterest.com/apps/
2. Create a new app
3. Go to **"Generate access token"**
4. Select scopes: `boards:read`, `pins:write`, `pins:read`
5. Copy token → save as `PINTEREST_ACCESS_TOKEN`
6. Run `python src/pinterest.py` to list your boards and get board ID
   → save as `PINTEREST_BOARD_ID`

### D) Amazon Associate ID
- Already in your Amazon affiliate dashboard
- It looks like: `yourname-21`
- Save as `AMAZON_ASSOCIATE_ID`

### E) Blog URL
- Your Blogger URL e.g. `codergadgetfinds.blogspot.com`
- Save as `BLOG_URL`

---

## 🚀 Step 2 — Deploy to GitHub (Free Hosting)

```bash
# 1. Create new GitHub repo (make it PRIVATE)
# 2. Push this project
git init
git add .
git commit -m "Initial affiliate bot"
git remote add origin https://github.com/YOURUSERNAME/affiliate-bot.git
git push -u origin main
```

---

## 🔐 Step 3 — Add Secrets to GitHub

1. Go to your GitHub repo
2. Click **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"** for each:

| Secret Name               | Value                    |
|--------------------------|--------------------------|
| `GEMINI_API_KEY`          | From Step 1A             |
| `GOOGLE_CREDENTIALS_JSON` | From Step 1B             |
| `BLOGGER_BLOG_ID`         | From Step 1B             |
| `PINTEREST_ACCESS_TOKEN`  | From Step 1C             |
| `PINTEREST_BOARD_ID`      | From Step 1C             |
| `AMAZON_ASSOCIATE_ID`     | From Step 1D             |
| `BLOG_URL`                | From Step 1E             |

---

## ✅ Step 4 — Test Run

1. Go to GitHub repo → **Actions** tab
2. Click **"Daily Affiliate Bot"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch the logs in real time
5. Check your Blogger and Pinterest after ~10 mins

---

## ⏰ Schedule

Bot runs automatically every day at **9:00 AM IST**.
- 20 blog posts published to Blogger
- 20 pins posted to Pinterest
- All linked with your Amazon affiliate ID
- Logs saved as GitHub Actions artifacts

To change the time, edit `.github/workflows/daily_bot.yml`:
```yaml
- cron: '30 3 * * *'   # 9 AM IST = 3:30 AM UTC
```
Use https://crontab.guru to calculate your time.

---

## 📁 Project Structure

```
affiliate-bot/
├── main.py                        # Master orchestrator
├── requirements.txt               # Python dependencies
├── src/
│   ├── keywords.py                # Google Trends keyword finder
│   ├── content.py                 # Gemini AI blog writer
│   ├── blogger.py                 # Blogger auto-publisher
│   ├── image_gen.py               # Pinterest pin image generator
│   └── pinterest.py               # Pinterest auto-pinner
├── logs/
│   └── run_log.json               # Daily run logs
└── .github/
    └── workflows/
        └── daily_bot.yml          # GitHub Actions scheduler
```

---

## 💰 Realistic Earnings Projection

| Month | Posts Published | Est. Monthly Visitors | Est. Earnings |
|-------|----------------|----------------------|---------------|
| 1     | 600            | 0–100                | ₹0            |
| 2     | 1,200          | 100–500              | ₹500–2,000    |
| 3     | 1,800          | 500–2,000            | ₹2,000–8,000  |
| 6     | 3,600          | 2,000–8,000          | ₹8,000–25,000 |
| 12    | 7,200          | 5,000–20,000         | ₹20,000–60,000|

> Pinterest content compounds — a pin made today can drive traffic for 2–3 years.

---

## ⚠️ Important Notes

1. **Amazon PA-API** — You need 3 sales in 180 days to keep access. Until then the bot uses Amazon search page links (still earns commission).
2. **Pinterest rate limits** — If you get rate limited, increase `DELAY_BETWEEN` in `main.py` from 15s to 30s.
3. **Affiliate disclosure** — Already included in every blog post (required by Amazon TOS).
4. **Content quality** — Gemini 1.5 Flash generates good content but review occasionally to ensure quality.
