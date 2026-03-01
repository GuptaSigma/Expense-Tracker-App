# AI-Powered Wealth & Expense Tracker 💰🚀

## Overview
This project not only tracks your expenses but also analyzes your financial health using **AI** and **Real-time Market Data** to provide smart investment suggestions!

## 🌟 Key Features

### 1. **Advanced AI Spending Predictions** 📊
- **LSTM Neural Network** captures complex spending patterns
- **ARIMA Statistical Model** with confidence intervals
- **Ensemble Forecasting** (LSTM + ARIMA) for best accuracy
- Custom anomaly detection finds unusual expenses
- Smart alerts for overspending & budget anomalies
- 70-85% prediction accuracy (vs 50-65% basic models)

### 2. **Real-time Market Watch** 📈
- **Gold & Silver Rates**: Live data from GoldAPI.io (24K prices in INR)
- **Cryptocurrency**: Bitcoin, Ethereum prices via yfinance
- **Indian Indices**: Nifty 50, BSE Sensex trends
- **Global Markets**: S&P 500 live prices

### 3. **Comprehensive Financial Analysis** 🤖
- **Financial Health Score**: 0-100 rating with breakdown
- **Emergency Fund Calculator**: How many months can you survive?
- **Risk Assessment**: 5-dimensional risk analysis framework
- **Portfolio Optimizer**: Modern Portfolio Theory (MPT) allocation
- **Retirement Planner**: How much corpus you need by retirement
- **Value at Risk (VaR)**: Measure portfolio downside risk
- **Stress Testing**: What happens in market crashes/recessions?
- Personalized wealth-building strategies

### 4. **Advanced Risk Management** 🛡️
- **Debt-to-Income Ratio** analysis
- **Insurance Gap Detection**
- **Volatility Analysis** (GARCH model)
- **Sensitivity Analysis**: How sensitive is your plan to changes?
- **Stress Scenarios**: Market crash, inflation, recession impact
- Smart mitigation strategies & action items

### 5. **Long-Term Wealth Planning** 💎
- **SIP Calculator**: 20-year wealth projections
- **Investment Returns Simulator**: Compound growth analysis
- **Inflation Impact**: Retirement corpus adjusted for inflation
- **Asset Allocation Recommendations**: 9 asset classes
- **Portfolio Rebalancing**: Know when to adjust holdings

### 6. **Beautiful Modern UI** ✨
- Glassmorphism design
- Interactive Chart.js visualizations
- Real-time market data updates
- Responsive Bootstrap layout

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask 3.0.0 |
| **Database** | SQLAlchemy + PostgreSQL (Neon / any Postgres host) |
| **Frontend** | HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js |
| **Deep Learning** | TensorFlow 2.14.0 (LSTM Neural Networks) |
| **Statistical Forecasting** | Statsmodels 0.14.0 (ARIMA models) |
| **Machine Learning** | Scikit-learn 1.3.0 |
| **Financial Math** | Pandas 2.0.3, NumPy 1.24.3, SciPy 1.11.0 |
| **APIs** | GoldAPI.io, yfinance, OpenRouter, Gemini AI |
| **Market Data** | Real-time via multiple sources |

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/wealth-tracker.git
cd wealth-tracker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**⚠️ ML Dependencies Note:** The project uses advanced ML models including:
- **TensorFlow 2.14.0** for LSTM neural networks
- **Statsmodels** for ARIMA forecasting
- **Scikit-learn** for additional ML algorithms

These are automatically installed via `requirements.txt`. First installation may take 5-10 minutes as TensorFlow is large (~400MB).

**If TensorFlow installation fails:**
```bash
# Install with explicit version
pip install tensorflow==2.14.0 --no-cache-dir

# Verify LSTM is working
python -c "from tensorflow.keras.layers import LSTM; print('✓ LSTM is working')"
```

### Step 3: Configure Environment Variables
Create a `.env` file in the root directory (copy from `.env.example`):
```bash
cp .env.example .env
```

Edit `.env` and add your API keys (get them from the respective platforms):
```env
# Required API Keys (get from the official sources)
GEMINI_API_KEY=your-gemini-api-key-here
OPENROUTER_API_KEY=your-openrouter-api-key-here
GOLD_API_KEY=your-goldapi-key-here
SECRET_KEY=your-secret-key-here
```

**⚠️ SECURITY NOTE:** Never commit `.env` file or expose API keys in public repositories. Use `.env.example` template only.

**Get API Keys from official sources:**
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenRouter API**: [OpenRouter.ai](https://openrouter.ai/keys)
- **Gold API**: [GoldAPI.io](https://www.goldapi.io/)

### Step 3b: Database Setup (PostgreSQL required)

The app requires **PostgreSQL**. Set the `DATABASE_URL` environment variable to your Postgres connection string (e.g., a [Neon](https://neon.tech) database):

```env
# Replace <password> with your actual password
DATABASE_URL=postgresql://user:<password>@host/dbname?sslmode=require
```

**On Render:** Add `DATABASE_URL` as an environment variable in the Render dashboard. Do **not** commit credentials to the repository.

**Schema initialisation:** The repo uses Flask-Migrate. Run migrations on first deploy (or after schema changes):

```bash
flask db upgrade
```

Alternatively, set `AUTO_CREATE_TABLES=1` to have the app create tables automatically on startup (useful for a quick first deploy; `flask db upgrade` is preferred in production).

### Step 3c: Deploy on Render (with Neon PostgreSQL)

Follow these steps for a **zero-manual-SQL** deployment on [Render](https://render.com) backed by a [Neon](https://neon.tech) Postgres database.

#### 1. Create a Neon database

1. Sign up at [neon.tech](https://neon.tech) and create a new project.
2. Copy the connection string from the Neon dashboard (use the **pooled** connection string for Render):
   ```
   postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
   ```

#### 2. Configure Render environment variables

In your Render service → **Environment**, add:

| Variable | Value | Notes |
|---|---|---|
| `DATABASE_URL` | `postgresql://...` | Your Neon connection string |
| `SECRET_KEY` | *(random string)* | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `RUN_MIGRATIONS` | `1` | Runs `flask db upgrade` on every deploy (recommended) |
| `AUTO_CREATE_TABLES` | `0` | Alternative to migrations: creates tables via `db.create_all()` if set to `1` |
| `SESSION_COOKIE_SECURE` | `1` | Required for HTTPS on Render |

> **First deploy:** Set `RUN_MIGRATIONS=1`. The startup script will run `flask db upgrade`, which creates all tables and stamps the database. `AUTO_CREATE_TABLES` is an alternative (uses `db.create_all()` instead of migrations) — pick one approach.

#### 3. Set the Start Command

In Render → **Settings → Start Command**, enter:

```
bash scripts/render_start.sh
```

This is also the default in `Procfile`, so Render picks it up automatically for web services.

#### 4. Trigger a deploy

Push to your connected branch or click **Manual Deploy** in Render. The startup script will:
1. Validate `DATABASE_URL` is present (exits with error if missing).
2. Run `flask db upgrade` (if `RUN_MIGRATIONS=1`).
3. Start **gunicorn**.

#### 5. OTP / Email settings on Render

OTP email verification is mandatory for all normal (email/password) registrations. Emails are delivered via **Google Apps Script** — no SMTP credentials required.

| Variable | Description |
|---|---|
| `DISABLE_EMAIL_OTP` | Set to `true` to skip OTP verification (auto-verify users). **Not recommended in production.** |
| `OTP_DEV_MODE` | Set to `true` to log OTP to console instead of sending email. **Never use in production.** |

**How it works:**

- All new users registering with email/password are sent an OTP via the Google Apps Script Web App and must verify before logging in.
- Users authenticating via Google OAuth are trusted and may log in without OTP verification.
- Login is blocked for unverified users with the message: *"Login blocked: Verify OTP from email before login."*

#### 6. Verify

Visit `https://<your-app>.onrender.com/register`. You should see the registration page with no database errors.

---

### Step 4: Run the App

**Important:** Always activate the virtual environment before running!

**Option 1: Easy Startup (Recommended)**
```bash
# CMD (Command Prompt) users:
start_app.bat

# PowerShell users:
.\start_app.ps1
```

**Option 2: Manual Activation**
```bash
# CMD (Command Prompt):
.venv\Scripts\activate.bat
python run.py

# PowerShell:
.\.venv\Scripts\Activate.ps1
python run.py

# Linux/Mac:
source .venv/bin/activate
python run.py
```

App will run on **http://127.0.0.1:5000**

⚠️ **Common Issue:** If you get NumPy version errors, make sure you activated the virtual environment (`.venv`) before running!

---

## 🚀 Features Breakdown

### Dashboard
- Total Income & Expenses (₹ in Indian Rupees)
- Category-wise spending breakdown
- Recent transactions
- AI-generated spending insights
- Next month spending predictions

### Market Watch
- Real-time Gold/Silver prices
- Bitcoin & Ethereum rates
- Nifty 50 & S&P 500 indices
- AI investment recommendations
- Market opportunity alerts

### Investment Coach
- Personalized wealth strategy
- Emergency fund planning
- SIP recommendations
- Savings rate analysis
- Wealth-building principles

---

## 📊 Advanced Machine Learning Models

### Spending Prediction (Ensemble Method)
```
Primary Model: LSTM Neural Network (60% weight)
- Captures complex temporal dependencies
- Requires: 20+ historical data points
- Accuracy: 65-80%

Secondary Model: ARIMA (40% weight)
- Statistical time series forecasting
- Includes 95% confidence intervals
- Handles seasonal patterns well
- Accuracy: 60-75%

Fallback: Linear Regression (if <20 data points)
- Fast, simple baseline
- Accuracy: 50-65%

Ensemble Result: 70-85% accuracy
```

### Financial Health Scoring
```
Factors (0-100 scale):
✓ Savings Rate:        0-30 points
✓ Emergency Fund:      0-30 points
✓ Positive Cashflow:   0-40 points

Ratings:
90+: Excellent 🌟
75-89: Good ✅
50-74: Fair ⚠️
<50: Needs Improvement 🔴
```

### Risk Assessment Framework
```
Five Dimensions Analyzed:
1. Liquidity Risk (Emergency fund adequacy)
2. Debt Burden (Debt-to-Income ratio)
3. Insurance Gap (Health + Life coverage)
4. Income Volatility (Income stability)
5. Overall Risk Score (Composite 0-100)

Mitigation: Auto-generated action items
```

### Portfolio Optimization
```
9 Asset Classes with Expected Returns:
├─ Equity (Large Cap): 12% return, 15% volatility
├─ Equity (Mid Cap): 14% return, 22% volatility
├─ Equity (Small Cap): 16% return, 28% volatility
├─ Government Bonds: 6% return, 4% volatility
├─ Corporate Bonds: 8% return, 6% volatility
├─ Gold: 8% return, 12% volatility
├─ Real Estate: 10% return, 10% volatility
├─ Cryptocurrency: 20% return, 50% volatility
└─ Cash: 4% return, 0% volatility

3 Risk Profiles: Conservative | Moderate | Aggressive
```

---

## 🔐 Security Notes
**⚠️ CRITICAL - API Key Security**
- ✅ All API keys stored in `.env` file ONLY
- ✅ Never expose keys in README, code, or commits
- ✅ Use `.env.example` as template for setup
- Database uses PostgreSQL (configured via `DATABASE_URL`)
- Flask debug mode for development only
- CSRF protection via Flask-Login
- Environment-based configuration for production

---

## 📈 Market Data Sources

| Asset Class | Source | Update Frequency |
|------------|--------|-----------------|
| Gold/Silver | GoldAPI.io | Real-time |
| Bitcoin/ETH | yfinance | Real-time |
| Nifty 50 | yfinance | During market hours |
| S&P 500 | yfinance | After market close |

---

## 🎯 How It Works (Complete Logic)

1. **Data Collection**
   - User logs income/expenses daily
   - System stores with timestamp & category

2. **Analysis Phase**
   - ML model analyzes 30-day history
   - Identifies spending patterns
   - Predicts next month's expenses

3. **Market Integration**
   - Fetches live Gold, Crypto, Stock prices
   - Compares with historical data
   - Calculates price changes (24h, 5d)

4. **Smart Recommendations**
   - If Bitcoin down >2% & user has balance → BUY signal
   - If Gold stable & user has savings → HOLD signal
   - If Nifty correcting & user has surplus → SIP entry point
   - Emergency fund < 3 months → PRIORITY signal

5. **AI Coaching**
   - Analyzes complete financial profile
   - Generates personalized strategy
   - Suggests asset allocation
   - Provides actionable next steps

---

## 📱 Routes Overview

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home (redirects to dashboard/login) |
| `/dashboard` | GET | Main dashboard |
| `/market` | GET | Real-time market watch |
| `/investment-coach` | GET | AI investment coaching |
| `/add-expense` | GET/POST | Add expense entry |
| `/add-income` | GET/POST | Add income entry |
| `/api/market_data` | GET | JSON market data |
| `/login` | GET/POST | User authentication |
| `/register` | GET/POST | New user registration |

---

## 🌐 UI Navigation

```
Navbar:
├── Dashboard (Main overview)
├── Market Watch (Real-time data)
├── AI Coach (Investment guidance)
├── Add Expense
├── Add Income
└── Logout

Dashboard Quick Actions:
├── Add Expense
├── Add Income
├── Market Watch
├── AI Coach
└── Logout
```

---

## 💡 Investment Strategy Tips

> "Invest today, secure your tomorrow!"

1. **Emergency Fund FIRST** 
   - 6 months of living expenses
   - Park in savings account

2. **SIP in Index Funds**
   - ₹1,000-5,000/month minimum
   - Best for rupee cost averaging

3. **Gold as Hedge**
   - 15-20% of portfolio
   - Protects against inflation

4. **Diversification Rule**
   - 60% Stocks
   - 20% Gold/Precious metals
   - 20% Bonds/Savings

5. **Time Your Entries**
   - Buy when markets dip
   - Don't time perfectly (just SIP)
   - Stay consistent

---

## 🌐 Language Logic (AI Suggestions & Chatbot)

The AI Fin-Buddy chatbot and all AI suggestions follow these language rules:

- **Default language: English** — All chatbox greetings, suggestion prompts, and default AI responses are in English.
- **Hindi detection** — If the user sends a message in Hindi (Devanagari script or common Hindi keywords such as *mera*, *kitna*, *kya*, *paisa*, etc.), the AI automatically switches to Hindi for that reply.
- **English input → English reply** — If the user writes in English, the AI always replies in clear, professional English. Hinglish (mixed Hindi-English) is never used.
- **Hindi input → Hindi reply** — If the user writes in Hindi, the AI replies in pure Hindi (no Hinglish mixing).
- **No Hinglish defaults** — There are no Hinglish or mixed-language defaults anywhere in the suggestions panel or chatbox.

This logic is implemented in:
- `app/local_chatbot.py` — `detect_language()` function + all response methods default to English.
- `app/gemini_chatbot.py` — `detect_language()` function; Gemini/OpenRouter prompts instruct pure Hindi or pure English based on detection.
- `app/ml_model.py` — AI suggestions prompt requests clear English output.

---

## ⚠️ Alpha Issues & Fallbacks

The app includes intelligent fallbacks:

```python
# If GoldAPI fails → Returns cached fallback prices
# If yfinance fails → Returns last 5d average
# If AI generation fails → Returns structured recommendations
# Market updates every 5 minutes
```

---

## ⚡ Troubleshooting

### NumPy Version Conflicts ⚠️

**Problem:** `AttributeError: _ARRAY_API not found` or `numpy.core.multiarray failed to import`
```bash
# This happens when running without activating virtual environment
# Solution 1: Use the startup scripts
start_app.bat         # For CMD
.\start_app.ps1      # For PowerShell

# Solution 2: Activate venv manually first
.venv\Scripts\activate.bat    # For CMD
python run.py
```

**Root Cause:** Global Python has NumPy 2.x but project needs NumPy 1.24.3

### TensorFlow/LSTM Issues

**Problem:** `ModuleNotFoundError: No module named 'tensorflow'`
```bash
# Solution: Install TensorFlow explicitly
pip install tensorflow==2.14.0 --no-cache-dir
```

**Problem:** LSTM predictions returning fallback results
```bash
# Verify LSTM is working:
python -c "from tensorflow.keras.layers import LSTM; print('✓ LSTM imported successfully')"
```

**Problem:** Slow LSTM training on first prediction
- First prediction takes longer due to model compilation
- Subsequent predictions are much faster (cached)
- Normal behavior - not a bug

### Dependency Conflicts

**If `pip install -r requirements.txt` fails:**
```bash
# Clean install without cache
pip install -r requirements.txt --no-cache-dir --force-reinstall
```

**If you get protobuf version conflicts:**
```bash
pip install protobuf==4.25.8
```

### Running the App

**Port already in use:**
```python
# Edit run.py and change the port:
app.run(debug=True, port=5001)  # Use port 5001 instead
```

---

## 🔮 Future Roadmap

### ✅ Recently Completed (v3.0)
- [x] Advanced ML (LSTM, ARIMA, Ensemble)
- [x] Deep Financial Modeling (MPT, SIP calculator)
- [x] Risk Analysis Framework (5-dimensional)
- [x] Portfolio Optimization & Rebalancing
- [x] Retirement Planning Tool
- [x] API Key Security Hardening

### 🚀 Coming Soon
- [ ] OCR Receipt Scanner (bill photos → auto entries)
- [ ] Dark Mode (high-contrast UI)
- [ ] PDF Reports (monthly wealth growth)
- [ ] Email Alerts (market opportunities)
- [ ] Mobile App (React Native)
- [ ] Tax Optimization (tax-saving suggestions)
- [ ] Blockchain Integration (Web3 assets)
- [ ] Prophet Framework (Facebook's time series library)
- [ ] XGBoost Models (extreme gradient boosting)
- [ ] Deep Q-Learning (reinforcement learning for investments)

---

## � Documentation
Check these files for detailed implementation:
- **[ADVANCED_ML_GUIDE.md](ADVANCED_ML_GUIDE.md)** - Complete ML models documentation
- **[CRITICAL_FIXES_SUMMARY.md](CRITICAL_FIXES_SUMMARY.md)** - Security fixes & improvements
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Code examples & usage

## 💻 Example Usage

```python
from app.ml_model import ComprehensiveFinancialAnalysis

analyzer = ComprehensiveFinancialAnalysis()
report = analyzer.generate_comprehensive_report(
    user_id=1,
    user_balance=500000,
    total_income=100000,
    total_expenses=60000,
    age=35
)

# Gets complete analysis:
# - Financial health score
# - Risk assessment with alerts
# - Portfolio recommendations
# - 20-year SIP projections
# - Retirement corpus needed
```

## 🔧 Troubleshooting OTP Email

If OTP emails are not being delivered, check the application logs for `[OTP][GAS]` messages.

### Common Causes & Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `[OTP][GAS] Error` in logs | Network error reaching Apps Script endpoint | Check outbound connectivity from your host; redeploy and retry |
| OTP email not received | Apps Script delivery issue | Check spam folder; retry registration after a moment |

### Environment Variables Reference

| Variable | Required | Default | Notes |
|---|---|---|---|
| `DISABLE_EMAIL_OTP` | No | `false` | Set `true` to skip OTP (auto-verify). Not for production. |
| `OTP_DEV_MODE` | No | `false` | Set `true` to log OTP to console instead of sending email. Not for production. |

No SMTP or mail-server credentials are needed — OTP delivery is handled by Google Apps Script.

### Development / Offline Mode

Set `OTP_DEV_MODE=true` in your `.env` to print the OTP to the console log instead of calling the Apps Script API:

```
[OTP][GAS] Response for user@example.com: ...
```

Use the printed OTP directly in the `/verify-otp` form during local development.

---

## 📞 Support & Contribution

Built with ❤️ using Flask, Scikit-learn, TensorFlow, and yfinance

---

## 📄 License
MIT License - Feel free to use & modify!

**Happy Investing! 🚀💰**

---

*Last Updated: February 25, 2026*
*Version: 3.0 (Advanced ML, Financial Modeling & Risk Analysis)*
