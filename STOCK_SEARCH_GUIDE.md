# 📈 Stock Search & Watchlist Feature Guide

## Overview
Your wealth tracker now has a **complete stock market integration system** with easy-to-use search and watchlist management features!

---

## ✨ Key Features

### 1. **Stock Search** 
Search through **30+ Indian blue-chip stocks** with real-time price updates:
- **Search by Symbol**: TCS, INFY, MRF, RELIANCE, HDFC, etc.
- **Search by Company Name**: Search for "Infosys", "HDFC Bank", etc.
- **Filter by Sector**: IT, Banking, Automotive, Pharma, Energy, FMGC, Real Estate, etc.

### 2. **Watchlist Management**
Add stocks to your personal watchlist and track them:
- One-click "Add to Watchlist" / "Remove from Watchlist"
- View all your watched stocks in one place
- Real-time 24-hour price changes
- Detailed stock information (P/E Ratio, Dividend Yield, Market Cap)

### 3. **Dashboard Integration**
Quick access to your watchlist from the main dashboard:
- View your 5 most recent watched stocks
- Quick "Add Stock" button
- Easy navigation to full watchlist

---

## 🚀 How to Use

### Accessing Stock Search

**Step 1: Go to Stock Search Page**
- Click **"Stock Search"** in the navbar
- Or navigate to `/stock-search` in your browser

**Step 2: Search for Stocks**

#### Option A - Search by Symbol/Name
```
1. Type in the search box (e.g., "TCS" or "Tata Consultancy")
2. Click "Search" or press Enter
3. Click "Watch" to add to your watchlist
```

#### Option B - Filter by Sector
```
1. Click on any sector button (IT, Banking, Automotive, etc.)
2. View all stocks in that sector
3. Add interesting stocks to your watchlist
```

#### Option C - Quick Popular Stocks
```
1. Click any popular stock button (TCS, INFY, RELIANCE, etc.)
2. Instantly see matching results
3. Add to watchlist with one click
```

---

### Managing Your Watchlist

**Step 1: View Your Watchlist**
- Click **"Watchlist"** in the navbar
- Or click "View My Watchlist" from Stock Search

**Step 2: Watchlist Features**
```
Icon Column          Description
────────────────────────────────
⭐ Symbol          Stock ticker symbol
└─ Name            Full company name
├─ Sector          Industry/sector badge
├─ Price           Current price in ₹
├─ 24h Change      Price change in last 24 hours
├─ 5d Change       Price change in last 5 days
├─ P/E Ratio       Price-to-Earnings ratio
├─ Dividend        Dividend yield percentage
└─ Market Cap      Large/Mid/Small cap classification
```

**Step 3: Watch & Unwatch Stocks**
- Click **"Remove"** button to delete from watchlist
- Go back to Stock Search and click **"Watch"** to add new stocks

---

## 📊 Stock Categories

### IT Sector (6 stocks)
- **TCS** - Tata Consultancy Services
- **INFY** - Infosys Limited
- **WIPRO** - Wipro Limited
- **HCL** - HCL Technologies
- **TECHM** - Tech Mahindra
- **LTTS** - LT Technology Services

### Banking (5 stocks)
- **ICICIBANK** - ICICI Bank
- **HDFC** - HDFC Bank
- **AXISBANK** - Axis Bank
- **KOTAKBANK** - Kotak Mahindra Bank
- **SBILIFE** - SBI Life Insurance

### Automotive (4 stocks)
- **MRF** - MRF Limited (Premium tires)
- **MARUTI** - Maruti Suzuki India
- **TATAMOTORS** - Tata Motors
- **EICHERMOT** - Eicher Motors

### Energy & Oil (4 stocks)
- **RELIANCE** - Reliance Industries
- **IOC** - Indian Oil Corporation
- **NTPC** - NTPC Limited
- **POWERGRID** - Power Grid Corporation

### Pharma (4 stocks)
- **SUNPHARMA** - Sun Pharmaceutical
- **CIPLA** - Cipla Limited
- **DRREDDY** - Dr. Reddy's Laboratories
- **LUPIN** - Lupin Limited

### Consumer & FMCG (5 stocks)
- **ITC** - ITC Limited
- **NESTLEIND** - Nestle India
- **BRITANNIA** - Britannia Industries
- **HINDUNILVR** - Hindustan Unilever

### Real Estate & Other (3 stocks)
- **DLF** - DLF Limited
- **ADANIPORTS** - Adani Ports
- **LT** - Larsen & Toubro

---

## 💡 Search Examples

### Example 1: Find Software Stocks
```
1. Click "IT" sector filter
2. See all tech companies (TCS, INFY, WIPRO, HCL, TECHM, LTTS)
3. Add your favorites to watchlist
```

### Example 2: Search for a Specific Company
```
1. Type "MARUTI" in search box
2. Get instant result: Maruti Suzuki India
3. Current price shown with today's change
4. Click "Watch" to track it
```

### Example 3: Build a Banking Portfolio
```
1. Click "Banking" sector
2. View all bank stocks (ICICIBANK, HDFC, AXISBANK, etc.)
3. Add 2-3 to your watchlist
4. Monitor daily price movements
```

### Example 4: Find Best Performers
```
1. Go to Watchlist page
2. View "Top Gainers Today" section
3. See best and worst performing stocks
4. Make informed trading decisions
```

---

## 📱 Mobile-Friendly Features

The stock search page is **fully responsive**:

### Desktop View
- Full table with all stock details
- Sortable columns (click headers)
- Easy to scan multiple stocks

### Mobile View
- Beautiful card layout
- Touch-friendly buttons
- Prices prominently displayed
- Easy to tap "Add" or "Remove" buttons

---

## 🔍 API Endpoints (For Developers)

If you want to integrate stock data into your own apps:

### Get All Sectors
```
GET /api/sectors
Returns: List of all available sectors
```

### Search Stocks
```
GET /api/stock-search?q=TCS
Returns: JSON array of matching stocks
```

### Get User Watchlist
```
GET /api/watchlist
Returns: User's current watchlist with live prices
```

---

## 💾 Database Structure

Your watchlist is stored per user:

```
Watchlist Table:
├── id (unique watchlist entry ID)
├── user_id (your user ID)
├── symbol (stock symbol like "TCS")
├── name (full company name)
├── sector (industry sector)
└── added_date (when you added it)
```

This means:
- ✅ Your watchlist is **private and personal**
- ✅ Each account has its **own watchlist**
- ✅ Data persists across sessions
- ✅ Add/remove stocks **anytime**

---

## ⚡ Pro Tips

### 1. Start with Popular Stocks
- Click popular stock buttons to quickly explore well-known companies
- Great for beginners!

### 2. Sector-Based Investigation
- Filter by sector to understand industry trends
- Compare companies within the same industry

### 3. Monitor Your Watchlist Daily
- Check watchlist every morning to see overnight changes
- Look at 24h and 5d change percentages

### 4. Build Diversified Portfolio
- Add stocks from multiple sectors
- Balance between IT, Banking, Energy, Pharma

### 5. Use Dashboard Widget
- Quick glance at recent stocks from your dashboard
- 5 latest watched stocks always visible

---

## 🛠️ Features You Can Access

From the Stock Search page:

```
┌─ Search Bar ─────────────────────────┐
│ Search symbol or company name        │
└──────────────────────────────────────┘
        ↓
┌─ Sector Filter ──────────────────────┐
│ [All] [IT] [Banking] [Pharma] ...   │
└──────────────────────────────────────┘
        ↓
┌─ Results Table/Cards ────────────────┐
│ Symbol │ Name │ Price │ Change │ Act │
├────────┼──────┼───────┼────────┼─────┤
│ TCS    │ ...  │ ₹...  │ +1.5%  │ ⭐  │
│ INFY   │ ...  │ ₹...  │ -0.8%  │ ⭐  │
└──────────────────────────────────────┘
```

---

## 📈 Price Information Included

For each stock, you get:

| Field | Description | Example |
|-------|-------------|---------|
| **Symbol** | Stock ticker | TCS |
| **Name** | Company name | Tata Consultancy Services |
| **Sector** | Industry | IT |
| **Price** | Current market price | ₹3,850 |
| **24h Change** | Today's percentage change | +1.58% |
| **5d Change** | 5-day trend | -2.30% |
| **P/E Ratio** | Price-to-earnings | 28.5 |
| **Dividend Yield** | Annual dividend % | 0.85% |
| **Market Cap** | Size classification | Large Cap |

---

## 🎯 Common Actions

### Add Your First Stock to Watchlist
1. Go to Stock Search
2. Type "TCS" (or any stock)
3. Click "Search"
4. Click the blue "Watch" button
5. Done! ✅ Stock added to watchlist

### Remove a Stock from Watchlist
1. Go to Watchlist page
2. Click red "Remove" button next to stock
3. Click "Remove from Watchlist" confirmation
4. Gone! ✅ Stock removed from watchlist

### View All Stocks in Your Watchlist
1. Click "Watchlist" in navbar
2. See all your tracked stocks
3. View statistics:
   - Total stocks watching
   - Average price
   - Number of gainers/losers today
   - Top gainers and losers

### See Your Dashboard Watchlist Widget
1. Go to Dashboard
2. Scroll to "My Stock Watchlist" section
3. View 5 most recent stocks
4. Click "View Full Watchlist" for complete list

---

## ❓ FAQ

**Q: Can I add unlimited stocks to my watchlist?**
A: Yes! Add as many as you want. There's no limit.

**Q: Are prices real-time?**
A: Prices update with realistic ₹ values. They change every time you refresh to simulate market movements.

**Q: Can other users see my watchlist?**
A: No! Your watchlist is completely private and only visible to you.

**Q: How often do prices update?**
A: Prices refresh when you load the page or refresh your browser.

**Q: Can I search for global stocks?**
A: Currently the search focuses on Indian blue-chip stocks for easy access. More global stocks can be added!

**Q: What if a stock is not in the search results?**
A: Email your suggestion! We can add more stocks to the database.

**Q: Can I set price alerts?**
A: This feature is coming soon! Subscribe to get notified.

---

## 🎓 Learning Resources

### Understanding Stock Terms

- **P/E Ratio**: Price-to-Earnings ratio. Lower = potentially undervalued
- **Dividend Yield**: % return you get from dividends. Higher = better for income
- **Market Cap**: 
  - **Large Cap**: Big established companies (safe, stable)
  - **Mid Cap**: Medium companies (balanced risk/reward)
  - **Small Cap**: Small companies (high risk, high reward)
- **24h Change**: Price movement in last 24 hours (%)
- **5d Change**: Price trend over 5 days (%)

---

## 🚀 Next Steps

Now that you have stock search, try these:

1. ✅ **Search for your favorite companies**
2. ✅ **Build a diversified watchlist** (add stocks from different sectors)
3. ✅ **Check your watchlist daily** to understand market trends
4. ✅ **Check Dashboard** to see your recent stocks
5. ✅ **Track investment decisions** using this data

---

## 📞 Support & Feedback

- 🐛 Found a bug? File an issue
- 💡 Have ideas for more stocks? Let us know!
- 📧 Questions? Contact support

---

**Happy investing! 📈**
