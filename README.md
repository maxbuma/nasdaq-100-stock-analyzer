# NASDAQ-100 Stock Analyzer 📈

An advanced technical analysis tool that scans all NASDAQ-100 stocks for buy-and-hold opportunities using multiple indicators.

## 🎯 Features

- **Complete NASDAQ-100 Coverage**: Analyzes all 102 stocks
- **Advanced Technical Analysis**: 
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Support/Resistance Levels
  - Golden/Death Cross Detection
  - Volume Analysis
- **Smart Scoring System**: Ranks opportunities by strength
- **Email Alerts**: Automatic notifications for top opportunities
- **No Mixed Signals**: Filters out conflicting indicators

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
4. The analyzer will run automatically every weekday at 9:30 AM EST

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

## 📈 Technical Indicators Explained

- **RSI < 30**: Oversold (potential buy)
- **RSI > 70**: Overbought (potential sell)
- **MACD Crossover**: Momentum change
- **Bollinger Bands**: Volatility and mean reversion
- **Golden Cross**: 50 MA crosses above 200 MA (bullish)
- **Support/Resistance**: Key price levels

## ⚠️ Disclaimer

This tool is for educational purposes only. Not financial advice. Always do your own research before making investment decisions.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use and modify!