# NASDAQ-100 Stock Analyzer 📈

An advanced technical analysis tool that scans all NASDAQ-100 stocks for buy-and-hold opportunities using multiple indicators and a sophisticated scoring system.

## 🎯 Features

- **Complete NASDAQ-100 Coverage**: Analyzes all 102 stocks daily
- **Advanced Technical Analysis**: 
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Support/Resistance Levels
  - Golden/Death Cross Detection
  - Volume Analysis
  - Price Momentum
- **Intelligent Scoring System**: Multi-factor scoring with signal strength weighting
- **Daily Email Alerts**: One comprehensive email every market day at 9:35 AM EST
- **No Mixed Signals**: Filters out conflicting indicators to avoid false positives
- **Buy-and-Hold Focus**: Optimized for 1-2 month investment horizons

## 🚀 Quick Start

### Option 1: Run Locally
```bash
# Clone the repository
git clone [your-repo-url]
cd stock-analyzer

# Install dependencies
pip install -r requirements.txt

# Set up your email credentials in config.py
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"

# Run the analyzer
python NASDAQ-100-2.py
```

### Option 2: Automated Daily Analysis (GitHub Actions)
1. Fork this repository
2. Go to Settings → Secrets and Variables → Actions
3. Add these secrets:
   - `EMAIL_ADDRESS`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail app password
4. The analyzer will run automatically every weekday at 9:35 AM EST (5 minutes after market open)

### Option 3: Run in Browser (Replit)
1. Go to [Replit](https://replit.com)
2. Import this GitHub repository
3. Update config.py with your credentials
4. Click "Run"

## 📊 Sample Output

```
🎯 TOP OPPORTUNITIES:

1. AMGN - Amgen Inc.:
Score: 11
Price: $278.52
RSI: 29.5
Signals:
  • 🟢 OVERSOLD: RSI 29.5 - Strong Buy Zone
  • 🟢 BOLLINGER OVERSOLD - Near Lower Band
  • 🟢 NEAR SUPPORT - Good risk/reward
  • 🟢 BULLISH TREND - 50 MA above 200 MA
```

## 🔧 Configuration

### Email Setup (Gmail)
1. Enable 2-factor authentication
2. Generate an app password: Google Account → Security → App passwords
3. Use the app password in `EMAIL_PASSWORD`

### Customization
- Modify `COMPANY_NAMES` to add/remove stocks
- Adjust scoring thresholds in `analyze_stocks()`
- Change email frequency in `.github/workflows/stock-analyzer.yml`

## 🧮 Scoring System Explained

The analyzer uses a sophisticated multi-factor scoring system designed for buy-and-hold opportunities. Each stock receives a score based on technical indicators, with higher scores indicating stronger buy signals.

### 📊 Scoring Components

#### RSI Analysis (Relative Strength Index)
- **RSI < 30**: +4 points - 🟢 **Strong Buy Zone** (Severely oversold)
- **RSI 30-40**: +2 points - 🟡 **Approaching Oversold** (Good entry opportunity)
- **RSI > 70**: -3 points - 🔴 **Overbought** (Avoid buying)

#### MACD Analysis (Moving Average Convergence Divergence)
- **Bullish Crossover**: +3 points - 🟢 **Momentum Turning Up** (MACD line crosses above signal line)
- **MACD Above Signal**: +1 point - 🟡 **Positive Momentum** (Upward momentum confirmed)
- **Bearish Crossover**: -2 points - 🔴 **Momentum Turning Down** (Sell signal)

#### Bollinger Bands Analysis
- **Near Lower Band** (Position < 0.2): +3 points - 🟢 **Oversold** (Price near bottom of range)
- **Near Upper Band** (Position > 0.8): -2 points - 🔴 **Overbought** (Price near top of range)
- **Bollinger Squeeze**: +1 point - ⚡ **Breakout Potential** (Low volatility, potential big move)

#### Support/Resistance Analysis
- **Near Support** (Within 5%): +2 points - 🟢 **Good Risk/Reward** (Strong floor for price)
- **Near Resistance** (Within 5%): -1 point - 🔴 **Potential Ceiling** (May face selling pressure)

#### Moving Average Trend Analysis
- **50 MA > 200 MA**: +2 points - 🟢 **Bullish Trend** (Long-term uptrend confirmed)
- **50 MA < 200 MA**: -1 point - 🔴 **Bearish Trend** (Long-term downtrend)

#### Golden/Death Cross Detection
- **Golden Cross**: +4 points - 🌟 **Major Bullish Signal** (50 MA crosses above 200 MA)
- **Death Cross**: -4 points - 💀 **Major Bearish Signal** (50 MA crosses below 200 MA)

#### Volume Confirmation
- **High Volume + Bullish Signals**: +2 points - 📈 **Strong Confirmation** (Institutional interest)
- **High Volume + Bearish Signals**: -1 point - 📉 **Warning** (Selling pressure)

#### Momentum Confirmation
- **Bullish Momentum + Buy Signals**: +1 point - 🚀 **Momentum Confirmed**
- **Bearish Momentum**: -1 point - 📉 **Downward Pressure**

### 🎯 Signal Quality Control

#### Mixed Signal Penalty
- **Conflicting Indicators**: -2 points - ⚠️ **Mixed Signals** (Reduces false positives)

#### Minimum Thresholds
- **Top Opportunities**: Score ≥ 4 (Only the strongest signals)
- **Good Opportunities**: Score ≥ 2 + More buy signals than sell signals
- **Email Alerts**: Only sent for stocks with clear directional bias

### 📈 Score Interpretation

| Score Range | Signal Strength | Action |
|-------------|----------------|---------|
| **8-15** | 🟢 **Very Strong Buy** | High conviction opportunity |
| **4-7** | 🟡 **Strong Buy** | Good opportunity with multiple confirmations |
| **2-3** | 🔵 **Moderate Buy** | Decent opportunity, watch closely |
| **0-1** | ⚪ **Neutral** | No clear signal |
| **-1 to -3** | 🟠 **Caution** | Mixed or weak bearish signals |
| **-4 or lower** | 🔴 **Avoid** | Strong bearish signals |

### 🎪 Example: High-Scoring Stock

```
AMGN - Amgen Inc. (Score: 11)
• 🟢 OVERSOLD: RSI 29.5 (+4 points)
• 🟢 BOLLINGER OVERSOLD (+3 points)  
• 🟢 NEAR SUPPORT (+2 points)
• 🟢 BULLISH TREND (+2 points)
• 📈 HIGH VOLUME CONFIRMATION (+2 points)
• ⚡ BOLLINGER SQUEEZE (+1 point)
• 📉 BEARISH MOMENTUM (-1 point)
• ⚠️ MIXED SIGNALS (-2 points)
```

This scoring system ensures you only receive alerts for stocks with genuine technical strength and clear directional bias, perfect for buy-and-hold strategies.

## 📈 Technical Indicators Reference

- **RSI**: Measures overbought/oversold conditions (0-100 scale)
- **MACD**: Shows relationship between two moving averages (momentum indicator)
- **Bollinger Bands**: Price channels based on standard deviation (volatility indicator)
- **Golden Cross**: 50-day MA crosses above 200-day MA (major bullish signal)
- **Support/Resistance**: Key price levels where stocks tend to bounce or stall

## ⚠️ Disclaimer

This tool is for educational purposes only. Not financial advice. Always do your own research before making investment decisions.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use and modify!
