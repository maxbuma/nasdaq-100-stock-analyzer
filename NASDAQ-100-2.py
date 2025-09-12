import yfinance as yf
import pandas as pd
import numpy as np
import yagmail
from datetime import datetime
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

# Complete NASDAQ-100 stocks
COMPANY_NAMES = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'GOOGL': 'Alphabet Inc.',
    'GOOG': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'META': 'Meta Platforms Inc.',
    'NVDA': 'NVIDIA Corporation',
    'TSLA': 'Tesla Inc.',
    'AVGO': 'Broadcom Inc.',
    'COST': 'Costco Wholesale Corporation',
    'NFLX': 'Netflix Inc.',
    'TMUS': 'T-Mobile US Inc.',
    'ASML': 'ASML Holding N.V.',
    'AMD': 'Advanced Micro Devices Inc.',
    'PEP': 'PepsiCo Inc.',
    'LIN': 'Linde plc',
    'CSCO': 'Cisco Systems Inc.',
    'ADBE': 'Adobe Inc.',
    'QCOM': 'QUALCOMM Incorporated',
    'TXN': 'Texas Instruments Incorporated',
    'INTU': 'Intuit Inc.',
    'ISRG': 'Intuitive Surgical Inc.',
    'CMCSA': 'Comcast Corporation',
    'BKNG': 'Booking Holdings Inc.',
    'AMGN': 'Amgen Inc.',
    'HON': 'Honeywell International Inc.',
    'VRTX': 'Vertex Pharmaceuticals Incorporated',
    'ADP': 'Automatic Data Processing Inc.',
    'PANW': 'Palo Alto Networks Inc.',
    'SBUX': 'Starbucks Corporation',
    'GILD': 'Gilead Sciences Inc.',
    'MU': 'Micron Technology Inc.',
    'ADI': 'Analog Devices Inc.',
    'INTC': 'Intel Corporation',
    'LRCX': 'Lam Research Corporation',
    'MDLZ': 'Mondelez International Inc.',
    'PYPL': 'PayPal Holdings Inc.',
    'KLAC': 'KLA Corporation',
    'REGN': 'Regeneron Pharmaceuticals Inc.',
    'SNPS': 'Synopsys Inc.',
    'CDNS': 'Cadence Design Systems Inc.',
    'MAR': 'Marriott International Inc.',
    'MRVL': 'Marvell Technology Inc.',
    'ORLY': 'O\'Reilly Automotive Inc.',
    'CSX': 'CSX Corporation',
    'FTNT': 'Fortinet Inc.',
    'DASH': 'DoorDash Inc.',
    'ADSK': 'Autodesk Inc.',
    'ABNB': 'Airbnb Inc.',
    'ROP': 'Roper Technologies Inc.',
    'NXPI': 'NXP Semiconductors N.V.',
    'WDAY': 'Workday Inc.',
    'CPRT': 'Copart Inc.',
    'FANG': 'Diamondback Energy Inc.',
    'PAYX': 'Paychex Inc.',
    'ODFL': 'Old Dominion Freight Line Inc.',
    'AEP': 'American Electric Power Company Inc.',
    'FAST': 'Fastenal Company',
    'ROST': 'Ross Stores Inc.',
    'BKR': 'Baker Hughes Company',
    'KDP': 'Keurig Dr Pepper Inc.',
    'EA': 'Electronic Arts Inc.',
    'VRSK': 'Verisk Analytics Inc.',
    'DDOG': 'Datadog Inc.',
    'XEL': 'Xcel Energy Inc.',
    'EXC': 'Exelon Corporation',
    'CTSH': 'Cognizant Technology Solutions Corporation',
    'GEHC': 'GE HealthCare Technologies Inc.',
    'KHC': 'The Kraft Heinz Company',
    'CCEP': 'Coca-Cola Europacific Partners PLC',
    'TEAM': 'Atlassian Corporation',
    'CSGP': 'CoStar Group Inc.',
    'IDXX': 'IDEXX Laboratories Inc.',
    'TTWO': 'Take-Two Interactive Software Inc.',
    'ZS': 'Zscaler Inc.',
    'ANSS': 'ANSYS Inc.',
    'ON': 'ON Semiconductor Corporation',
    'DXCM': 'DexCom Inc.',
    'CDW': 'CDW Corporation',
    'WBD': 'Warner Bros. Discovery Inc.',
    'BIIB': 'Biogen Inc.',
    'GFS': 'GlobalFoundries Inc.',
    'MDB': 'MongoDB Inc.',
    'ARM': 'Arm Holdings plc',
    'ILMN': 'Illumina Inc.',
    'MRNA': 'Moderna Inc.',
    'SMCI': 'Super Micro Computer Inc.',
    'WBA': 'Walgreens Boots Alliance Inc.',
    'CRWD': 'CrowdStrike Holdings Inc.',
    'DLTR': 'Dollar Tree Inc.',
    'MNST': 'Monster Beverage Corporation',
    'LULU': 'Lululemon Athletica Inc.',
    'MCHP': 'Microchip Technology Incorporated',
    'SIRI': 'Sirius XM Holdings Inc.',
    'PCAR': 'PACCAR Inc',
    'ALGN': 'Align Technology Inc.',
    'MELI': 'MercadoLibre Inc.',
    'LCID': 'Lucid Group Inc.',
    'RIVN': 'Rivian Automotive Inc.',
    'JD': 'JD.com Inc.',
    'PDD': 'PDD Holdings Inc.',
    'BIDU': 'Baidu Inc.'
}

STOCKS_TO_MONITOR = list(COMPANY_NAMES.keys())

# Email configuration
RECEIVER_EMAIL = "maxbuma5@gmail.com"
EMAIL_SUBJECT = "Daily Stock Analysis - Top Opportunities"

def get_stock_data(ticker, period="1y", interval="1d", max_retries=3):
    """Fetch stock data using yfinance with enhanced error handling"""
    import time
    import requests
    
    # Set up session with headers to avoid blocking
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching {ticker} (attempt {attempt + 1})...", end=' ')
            
            # Create ticker with custom session
            stock = yf.Ticker(ticker, session=session)
            
            # Add delay between requests
            if attempt > 0:
                time.sleep(3 + attempt)  # Increasing delay
            
            # Try different periods if the main one fails
            periods_to_try = [period, "6mo", "3mo", "1mo"] if period == "1y" else [period]
            
            for p in periods_to_try:
                try:
                    df = stock.history(period=p, interval=interval, timeout=30)
                    
                    if not df.empty and len(df) > 50:  # Need enough data for analysis
                        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                        if all(col in df.columns for col in required_columns):
                            print(f"Success! Got {len(df)} days of data (period: {p})")
                            return df
                    
                except Exception as period_error:
                    print(f"Period {p} failed: {period_error}")
                    continue
            
            print(f"No valid data for {ticker}")
            if attempt < max_retries - 1:
                print(f"Retrying in {3 + attempt} seconds...")
                time.sleep(3 + attempt)
            
        except Exception as e:
            print(f"Error: {str(e)[:100]}...")
            if attempt < max_retries - 1:
                print(f"Retrying in {3 + attempt} seconds...")
                time.sleep(3 + attempt)
    
    print(f"Failed to fetch {ticker} after {max_retries} attempts")
    return None

def calculate_rsi(data, periods=14):
    """Calculate RSI for a given stock dataframe"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=periods).mean()
    avg_loss = loss.rolling(window=periods).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def analyze_volume(data):
    """Analyze volume patterns and trends"""
    try:
        recent_volume = data['Volume'].tail(20)
        current_volume = recent_volume.iloc[-1]
        avg_volume = recent_volume.mean()
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        
        return {
            'current_volume': current_volume,
            'avg_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'high_volume': volume_ratio > 1.5
        }
    except Exception as e:
        print(f"Volume analysis error: {e}")
        return None

def check_golden_cross(data):
    """Check for Golden Cross and Death Cross patterns"""
    try:
        last_two_days = data[['MA50', 'MA200']].tail(2)
        if last_two_days['MA50'].iloc[0] < last_two_days['MA200'].iloc[0] and \
           last_two_days['MA50'].iloc[1] > last_two_days['MA200'].iloc[1]:
            return "GOLDEN CROSS"
        elif last_two_days['MA50'].iloc[0] > last_two_days['MA200'].iloc[0] and \
             last_two_days['MA50'].iloc[1] < last_two_days['MA200'].iloc[1]:
            return "DEATH CROSS"
        return None
    except Exception as e:
        print(f"Error checking cross: {e}")
        return None

def calculate_macd(data, fast=12, slow=26, signal=9):
    """Calculate MACD indicator"""
    try:
        ema_fast = data['Close'].ewm(span=fast).mean()
        ema_slow = data['Close'].ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd': macd_line.iloc[-1],
            'signal': signal_line.iloc[-1],
            'histogram': histogram.iloc[-1],
            'bullish_crossover': macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2],
            'bearish_crossover': macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]
        }
    except Exception as e:
        print(f"Error calculating MACD: {e}")
        return None

def calculate_bollinger_bands(data, window=20, std_dev=2):
    """Calculate Bollinger Bands"""
    try:
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        
        current_price = data['Close'].iloc[-1]
        bb_position = (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])
        
        return {
            'upper': upper_band.iloc[-1],
            'middle': rolling_mean.iloc[-1],
            'lower': lower_band.iloc[-1],
            'position': bb_position,
            'oversold': bb_position < 0.2,  # Near lower band
            'overbought': bb_position > 0.8,  # Near upper band
            'squeeze': (upper_band.iloc[-1] - lower_band.iloc[-1]) / rolling_mean.iloc[-1] < 0.1
        }
    except Exception as e:
        print(f"Error calculating Bollinger Bands: {e}")
        return None

def find_support_resistance(data, window=20):
    """Find recent support and resistance levels"""
    try:
        recent_data = data.tail(window)
        current_price = data['Close'].iloc[-1]
        
        # Find recent highs and lows
        resistance = recent_data['High'].max()
        support = recent_data['Low'].min()
        
        # Calculate distance from support/resistance
        resistance_distance = (resistance - current_price) / current_price
        support_distance = (current_price - support) / current_price
        
        return {
            'resistance': resistance,
            'support': support,
            'near_support': support_distance < 0.05,  # Within 5% of support
            'near_resistance': resistance_distance < 0.05,  # Within 5% of resistance
            'support_distance': support_distance,
            'resistance_distance': resistance_distance
        }
    except Exception as e:
        print(f"Error finding support/resistance: {e}")
        return None

def calculate_price_momentum(data, short_window=10, long_window=30):
    """Calculate price momentum indicators"""
    try:
        short_ma = data['Close'].rolling(window=short_window).mean()
        long_ma = data['Close'].rolling(window=long_window).mean()
        current_price = data['Close'].iloc[-1]
        
        # Price relative to moving averages
        price_vs_short = (current_price - short_ma.iloc[-1]) / short_ma.iloc[-1]
        price_vs_long = (current_price - long_ma.iloc[-1]) / long_ma.iloc[-1]
        
        # Recent price action
        recent_change = (data['Close'].iloc[-1] - data['Close'].iloc[-5]) / data['Close'].iloc[-5]
        
        return {
            'short_ma': short_ma.iloc[-1],
            'long_ma': long_ma.iloc[-1],
            'price_vs_short': price_vs_short,
            'price_vs_long': price_vs_long,
            'recent_change': recent_change,
            'bullish_momentum': price_vs_short > 0 and price_vs_long > 0 and recent_change > 0,
            'bearish_momentum': price_vs_short < 0 and price_vs_long < 0 and recent_change < 0
        }
    except Exception as e:
        print(f"Error calculating momentum: {e}")
        return None

def get_market_timing():
    """Determine current market timing based on EST time"""
    import os
    from datetime import datetime, timezone, timedelta
    
    # Get EST time
    est = timezone(timedelta(hours=-5))
    current_time = datetime.now(est)
    hour = current_time.hour
    minute = current_time.minute
    
    # Check environment variable first (from GitHub Actions)
    timing = os.environ.get('MARKET_TIMING', '')
    if timing:
        return timing
    
    # Determine timing based on EST hour
    if hour == 9 and minute < 30:
        return "pre-market"
    elif hour == 9 and minute >= 30:
        return "market-open"
    elif 10 <= hour <= 15:
        return "market-hours"
    elif hour == 16:
        return "market-close"
    else:
        return "after-hours"

def send_email_alert(top_opportunities):
    """Send email with top stock opportunities"""
    try:
        # Initialize yagmail with credentials from config
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Determine market timing for email subject
        timing = get_market_timing()
        timing_labels = {
            "pre-market": "Pre-Market Analysis",
            "market-open": "Market Open Opportunities", 
            "market-hours": "Mid-Day Update",
            "market-close": "Market Close Summary",
            "after-hours": "After-Hours Analysis"
        }
        
        subject = f"NASDAQ-100 {timing_labels.get(timing, 'Stock Analysis')} - {len(top_opportunities)} Opportunities"
        
        # Format the email content
        email_body = [
            f"🚀 NASDAQ-100 Stock Analysis Report",
            f"📅 {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p EST')}",
            f"⏰ {timing_labels.get(timing, 'Analysis')}\n",
            f"🎯 TOP {min(len(top_opportunities), 10)} OPPORTUNITIES:\n"
        ]
        
        for idx, stock in enumerate(top_opportunities[:10], 1):
            stock_info = [
                f"\n{idx}. {stock['ticker']} - {stock['company_name']}",
                f"Price: ${stock['price']:.2f}",
                f"RSI: {stock['rsi']:.2f}",
                f"Score: {stock['score']}",
                "Signals:",
                *[f"  • {signal}" for signal in stock['signals']],
                "-------------------"
            ]
            email_body.extend(stock_info)
        
        # Add footer with timing info
        email_body.extend([
            "\n" + "="*50,
            f"📊 Analysis completed at {datetime.now().strftime('%I:%M %p EST')}",
            f"🔄 Next analysis: {get_next_analysis_time()}",
            f"⚙️ Automated by NASDAQ-100 Stock Analyzer",
            "📈 Happy Trading!"
        ])
        
        # Send the email
        yag.send(
            to=RECEIVER_EMAIL,
            subject=subject,
            contents='\n'.join(email_body)
        )
        print(f"📧 Email alert sent successfully! Subject: {subject}")
    except Exception as e:
        print(f"Error sending email: {e}")

def get_next_analysis_time():
    """Get the next scheduled analysis time"""
    timing = get_market_timing()
    
    next_times = {
        "pre-market": "9:35 AM EST (Market Open)",
        "market-open": "12:00 PM EST (Mid-Day)",
        "market-hours": "4:05 PM EST (Market Close)", 
        "market-close": "9:00 AM EST Tomorrow (Pre-Market)",
        "after-hours": "9:00 AM EST Tomorrow (Pre-Market)"
    }
    
    return next_times.get(timing, "Next scheduled run")

def analyze_stocks(stock_list):
    """Analyze stocks with comprehensive technical analysis for buy-and-hold opportunities"""
    results = []
    failed_tickers = []
    successful_tickers = []
    
    for i, ticker in enumerate(stock_list, 1):
        try:
            company_name = COMPANY_NAMES.get(ticker, 'Unknown Company')
            print(f"\n[{i}/{len(stock_list)}] Analyzing {ticker} - {company_name}...")
            
            stock_data = get_stock_data(ticker)
            
            if stock_data is not None and not stock_data.empty:
                # Calculate all technical indicators
                stock_data['RSI'] = calculate_rsi(stock_data)
                stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
                stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
                
                current_rsi = stock_data['RSI'].iloc[-1]
                current_price = stock_data['Close'].iloc[-1]
                volume_data = analyze_volume(stock_data)
                macd_data = calculate_macd(stock_data)
                bb_data = calculate_bollinger_bands(stock_data)
                sr_data = find_support_resistance(stock_data)
                momentum_data = calculate_price_momentum(stock_data)
                
                # Initialize scoring - focused on buy-and-hold opportunities
                score = 0
                signals = []
                buy_signals = 0  # Count of bullish signals
                sell_signals = 0  # Count of bearish signals
                
                # RSI Analysis - Key for finding undervalued entries
                if current_rsi < 30:
                    score += 4
                    buy_signals += 1
                    signals.append(f"🟢 OVERSOLD: RSI {current_rsi:.1f} - Strong Buy Zone")
                elif current_rsi < 40:
                    score += 2
                    buy_signals += 1
                    signals.append(f"🟡 APPROACHING OVERSOLD: RSI {current_rsi:.1f}")
                elif current_rsi > 70:
                    score -= 3
                    sell_signals += 1
                    signals.append(f"🔴 OVERBOUGHT: RSI {current_rsi:.1f} - Avoid")
                
                # MACD Analysis - Momentum confirmation
                if macd_data:
                    if macd_data['bullish_crossover']:
                        score += 3
                        buy_signals += 1
                        signals.append("🟢 MACD BULLISH CROSSOVER - Momentum Turning Up")
                    elif macd_data['macd'] > macd_data['signal'] and macd_data['histogram'] > 0:
                        score += 1
                        buy_signals += 1
                        signals.append("🟡 MACD Above Signal - Positive Momentum")
                    elif macd_data['bearish_crossover']:
                        score -= 2
                        sell_signals += 1
                        signals.append("🔴 MACD BEARISH CROSSOVER - Momentum Turning Down")
                
                # Bollinger Bands - Value opportunities
                if bb_data:
                    if bb_data['oversold']:
                        score += 3
                        buy_signals += 1
                        signals.append(f"🟢 BOLLINGER OVERSOLD - Near Lower Band ({bb_data['position']:.2f})")
                    elif bb_data['overbought']:
                        score -= 2
                        sell_signals += 1
                        signals.append(f"🔴 BOLLINGER OVERBOUGHT - Near Upper Band ({bb_data['position']:.2f})")
                    
                    if bb_data['squeeze']:
                        score += 1
                        signals.append("⚡ BOLLINGER SQUEEZE - Breakout Potential")
                
                # Support/Resistance Analysis
                if sr_data:
                    if sr_data['near_support']:
                        score += 2
                        buy_signals += 1
                        signals.append(f"🟢 NEAR SUPPORT - ${sr_data['support']:.2f} ({sr_data['support_distance']:.1%} away)")
                    elif sr_data['near_resistance']:
                        score -= 1
                        sell_signals += 1
                        signals.append(f"🔴 NEAR RESISTANCE - ${sr_data['resistance']:.2f} ({sr_data['resistance_distance']:.1%} away)")
                
                # Moving Average Analysis - Trend confirmation
                if stock_data['MA50'].iloc[-1] > stock_data['MA200'].iloc[-1]:
                    score += 2
                    buy_signals += 1
                    signals.append("🟢 BULLISH TREND - 50 MA above 200 MA")
                else:
                    score -= 1
                    sell_signals += 1
                    signals.append("🔴 BEARISH TREND - 50 MA below 200 MA")
                
                # Golden/Death Cross - Major trend changes
                cross = check_golden_cross(stock_data)
                if cross == "GOLDEN CROSS":
                    score += 4
                    buy_signals += 1
                    signals.append("🌟 GOLDEN CROSS - Major Bullish Signal!")
                elif cross == "DEATH CROSS":
                    score -= 4
                    sell_signals += 1
                    signals.append("💀 DEATH CROSS - Major Bearish Signal!")
                
                # Volume Confirmation
                if volume_data and volume_data['high_volume'] and buy_signals > sell_signals:
                    score += 2
                    signals.append(f"📈 HIGH VOLUME CONFIRMATION - {volume_data['volume_ratio']:.1f}x average")
                elif volume_data and volume_data['high_volume'] and sell_signals > buy_signals:
                    score -= 1
                    signals.append(f"📉 HIGH VOLUME WARNING - {volume_data['volume_ratio']:.1f}x average")
                
                # Momentum Confirmation
                if momentum_data:
                    if momentum_data['bullish_momentum'] and buy_signals > sell_signals:
                        score += 1
                        signals.append("🚀 BULLISH MOMENTUM CONFIRMED")
                    elif momentum_data['bearish_momentum']:
                        score -= 1
                        signals.append("📉 BEARISH MOMENTUM")
                
                # Avoid mixed signals - penalize conflicting indicators
                if buy_signals > 0 and sell_signals > 0:
                    if sell_signals >= buy_signals:
                        score -= 2
                        signals.append("⚠️ MIXED SIGNALS - Proceed with caution")
                
                # Only include stocks with clear signals
                if signals and (buy_signals > sell_signals or score >= 3):
                    results.append({
                        'ticker': ticker,
                        'company_name': company_name,
                        'price': current_price,
                        'rsi': current_rsi,
                        'ma50': stock_data['MA50'].iloc[-1],
                        'ma200': stock_data['MA200'].iloc[-1],
                        'volume_data': volume_data,
                        'macd_data': macd_data,
                        'bb_data': bb_data,
                        'sr_data': sr_data,
                        'momentum_data': momentum_data,
                        'score': score,
                        'buy_signals': buy_signals,
                        'sell_signals': sell_signals,
                        'signals': signals
                    })
                    print("✅ Strong signal detected!")
                    successful_tickers.append(ticker)
                else:
                    print("⚪ No clear opportunity.")
                    successful_tickers.append(ticker)
            else:
                print("❌ No data available")
                failed_tickers.append(ticker)
                    
        except Exception as e:
            print(f"❌ Error analyzing {ticker}: {e}")
            failed_tickers.append(ticker)
            continue
    
    # Print summary of data fetching
    print(f"\n📊 Data Fetching Summary:")
    print(f"✅ Successful: {len(successful_tickers)}")
    print(f"❌ Failed: {len(failed_tickers)}")
    if failed_tickers:
        print(f"Failed tickers: {', '.join(failed_tickers[:10])}{'...' if len(failed_tickers) > 10 else ''}")
    
    return results

def send_error_email(error_message):
    """Log error but don't send email - only send emails with real data"""
    print(f"❌ Analysis failed: {error_message}")
    print("📧 No email sent - only sending emails when real Yahoo Finance data is available")
    print("🔄 Will retry automatically at next scheduled time")
    print("💻 To get real data now, run the analyzer locally on your computer")

def main():
    print(f"\nStarting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Monitoring {len(STOCKS_TO_MONITOR)} stocks...")
    
    # Test yfinance connection first
    print("\n🔍 Testing yfinance connection...")
    test_data = get_stock_data("AAPL", period="1mo", max_retries=2)
    if test_data is not None:
        print(f"✅ yfinance working! AAPL current price: ${test_data['Close'].iloc[-1]:.2f}")
        print(f"\n📊 Starting full analysis...")
        results = analyze_stocks(STOCKS_TO_MONITOR)
    else:
        print("❌ yfinance connection failed! Trying alternative approach...")
        
        # Try a few different tickers to see if any work
        test_tickers = ["MSFT", "GOOGL", "TSLA", "NVDA"]
        working_ticker = None
        
        for test_ticker in test_tickers:
            print(f"Testing {test_ticker}...")
            test_data = get_stock_data(test_ticker, period="1mo", max_retries=1)
            if test_data is not None:
                working_ticker = test_ticker
                print(f"✅ {test_ticker} working! Proceeding with limited analysis...")
                break
        
        if working_ticker:
            # Analyze only a subset of stocks to avoid rate limiting
            limited_stocks = STOCKS_TO_MONITOR[:20]  # First 20 stocks only
            print(f"📊 Running limited analysis on {len(limited_stocks)} stocks...")
            results = analyze_stocks(limited_stocks)
        else:
            print("❌ Complete API failure - no email will be sent")
            send_error_email("Yahoo Finance API is completely unavailable")
            return
    
    if results:
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Get top opportunities (score >= 4 for buy-and-hold)
        top_opportunities = [r for r in results if r['score'] >= 4]
        good_opportunities = [r for r in results if r['score'] >= 2 and r['buy_signals'] > r['sell_signals']]
        
        # Print analysis results
        print("\n=== TECHNICAL ANALYSIS SIGNALS ===")
        
        # Print Top Opportunities
        if top_opportunities:
            print("\n🎯 TOP OPPORTUNITIES:")
            for idx, result in enumerate(top_opportunities[:10], 1):
                print(f"\n{idx}. {result['ticker']} - {result['company_name']}:")
                print(f"Score: {result['score']}")
                print(f"Price: ${result['price']:.2f}")
                print(f"RSI: {result['rsi']:.2f}")
                print(f"50-day MA: ${result['ma50']:.2f}")
                print(f"200-day MA: ${result['ma200']:.2f}")
                if result['volume_data']:
                    print(f"Volume: {result['volume_data']['volume_ratio']:.1f}x average")
                print("Signals:")
                for signal in result['signals']:
                    print(f"  • {signal}")
            
            # Send email alert for top opportunities
            try:
                send_email_alert(top_opportunities[:10])
            except Exception as e:
                print(f"Error sending email: {e}")
        else:
            print("\n📊 ALL DETECTED SIGNALS:")
            for idx, result in enumerate(results[:10], 1):
                print(f"\n{idx}. {result['ticker']} - {result['company_name']}:")
                print(f"Score: {result['score']}")
                print(f"Price: ${result['price']:.2f}")
                print(f"RSI: {result['rsi']:.2f}")
                print("Signals:")
                for signal in result['signals']:
                    print(f"  • {signal}")
        
        # Print Summary Statistics
        print("\n=== 📊 SUMMARY STATISTICS ===")
        print(f"Total stocks analyzed: {len(STOCKS_TO_MONITOR)}")
        print(f"Stocks with signals: {len(results)}")
        print(f"Top opportunities: {len(top_opportunities)}")
        
    else:
        print("\nNo significant technical signals detected.")

if __name__ == "__main__":
    main()
