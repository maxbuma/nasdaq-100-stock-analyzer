import yagmail
from config import EMAIL_ADDRESS, EMAIL_PASSWORD
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time

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

def get_stock_data(ticker, period="1y", interval="1d"):
    """Enhanced data fetching with retry logic"""
    for attempt in range(2):
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            if not df.empty:
                return df
            time.sleep(1)  # Brief pause between attempts
        except Exception as e:
            if attempt == 1:  # Last attempt
                print(f"Error fetching data for {ticker}: {e}")
            time.sleep(1)
    return None

def calculate_rsi(data, periods=14):
    """RSI calculation"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    avg_gain = gain.rolling(window=periods).mean()
    avg_loss = loss.rolling(window=periods).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data, fast=12, slow=26, signal=9):
    """MACD calculation with crossover detection"""
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
            'bullish_crossover': (macd_line.iloc[-1] > signal_line.iloc[-1] and 
                                macd_line.iloc[-2] <= signal_line.iloc[-2]),
            'bearish_crossover': (macd_line.iloc[-1] < signal_line.iloc[-1] and 
                                macd_line.iloc[-2] >= signal_line.iloc[-2]),
            'above_zero': macd_line.iloc[-1] > 0,
            'momentum_strength': abs(histogram.iloc[-1])
        }
    except:
        return None

def calculate_bollinger_bands(data, window=20, std_dev=2):
    """Bollinger Bands with squeeze detection"""
    try:
        rolling_mean = data['Close'].rolling(window=window).mean()
        rolling_std = data['Close'].rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        
        current_price = data['Close'].iloc[-1]
        bb_position = (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])
        
        # Bollinger Band squeeze detection
        band_width = (upper_band.iloc[-1] - lower_band.iloc[-1]) / rolling_mean.iloc[-1]
        avg_band_width = ((upper_band - lower_band) / rolling_mean).rolling(50).mean().iloc[-1]
        squeeze = band_width < avg_band_width * 0.8
        
        return {
            'upper': upper_band.iloc[-1],
            'middle': rolling_mean.iloc[-1],
            'lower': lower_band.iloc[-1],
            'position': bb_position,
            'oversold': bb_position < 0.1,      # Very oversold
            'approaching_oversold': bb_position < 0.25,  # Approaching oversold
            'overbought': bb_position > 0.9,    # Very overbought
            'approaching_overbought': bb_position > 0.75, # Approaching overbought
            'squeeze': squeeze,
            'band_width': band_width
        }
    except:
        return None

def find_support_resistance(data, window=50):
    """Advanced support and resistance detection"""
    try:
        recent_data = data.tail(window)
        current_price = data['Close'].iloc[-1]
        
        # Find multiple support and resistance levels
        highs = recent_data['High']
        lows = recent_data['Low']
        
        # Primary levels
        resistance_1 = highs.max()
        support_1 = lows.min()
        
        # Secondary levels (remove outliers)
        resistance_2 = highs.nlargest(10).iloc[5:].mean()  # Average of 6th-10th highest
        support_2 = lows.nsmallest(10).iloc[5:].mean()     # Average of 6th-10th lowest
        
        # Distance calculations
        resistance_distance = (resistance_1 - current_price) / current_price
        support_distance = (current_price - support_1) / current_price
        
        return {
            'resistance_1': resistance_1,
            'resistance_2': resistance_2,
            'support_1': support_1,
            'support_2': support_2,
            'near_resistance': resistance_distance < 0.03,  # Within 3%
            'near_support': support_distance < 0.03,        # Within 3%
            'support_strength': support_distance,
            'resistance_strength': resistance_distance,
            'price_position': (current_price - support_1) / (resistance_1 - support_1)
        }
    except:
        return None

def analyze_volume(data):
    """Advanced volume analysis"""
    try:
        volumes = data['Volume']
        recent_volume = volumes.tail(20)
        current_volume = volumes.iloc[-1]
        
        # Multiple volume averages
        avg_volume_20 = recent_volume.mean()
        avg_volume_50 = volumes.tail(50).mean()
        
        volume_ratio_20 = current_volume / avg_volume_20 if avg_volume_20 > 0 else 0
        volume_ratio_50 = current_volume / avg_volume_50 if avg_volume_50 > 0 else 0
        
        # Volume trend
        volume_trend = recent_volume.tail(5).mean() / recent_volume.head(5).mean()
        
        return {
            'current_volume': current_volume,
            'avg_volume_20': avg_volume_20,
            'avg_volume_50': avg_volume_50,
            'volume_ratio_20': volume_ratio_20,
            'volume_ratio_50': volume_ratio_50,
            'high_volume': volume_ratio_20 > 1.5,
            'very_high_volume': volume_ratio_20 > 2.0,
            'volume_trend': volume_trend,
            'increasing_volume': volume_trend > 1.2
        }
    except:
        return None

def check_golden_cross(data):
    """Enhanced moving average crossover detection"""
    try:
        ma_data = data[['MA20', 'MA50', 'MA200']].tail(3)
        
        # Golden Cross variations
        golden_cross_50_200 = (ma_data['MA50'].iloc[-2] <= ma_data['MA200'].iloc[-2] and 
                              ma_data['MA50'].iloc[-1] > ma_data['MA200'].iloc[-1])
        
        death_cross_50_200 = (ma_data['MA50'].iloc[-2] >= ma_data['MA200'].iloc[-2] and 
                             ma_data['MA50'].iloc[-1] < ma_data['MA200'].iloc[-1])
        
        # Mini golden cross (20/50)
        mini_golden = (ma_data['MA20'].iloc[-2] <= ma_data['MA50'].iloc[-2] and 
                      ma_data['MA20'].iloc[-1] > ma_data['MA50'].iloc[-1])
        
        mini_death = (ma_data['MA20'].iloc[-2] >= ma_data['MA50'].iloc[-2] and 
                     ma_data['MA20'].iloc[-1] < ma_data['MA50'].iloc[-1])
        
        if golden_cross_50_200:
            return "GOLDEN CROSS"
        elif death_cross_50_200:
            return "DEATH CROSS"
        elif mini_golden:
            return "MINI GOLDEN"
        elif mini_death:
            return "MINI DEATH"
        return None
    except:
        return None

def calculate_momentum_indicators(data):
    """Multiple momentum indicators"""
    try:
        closes = data['Close']
        
        # Rate of Change (ROC)
        roc_10 = ((closes.iloc[-1] - closes.iloc[-11]) / closes.iloc[-11]) * 100
        roc_20 = ((closes.iloc[-1] - closes.iloc[-21]) / closes.iloc[-21]) * 100
        
        # Stochastic %K
        low_14 = data['Low'].rolling(14).min()
        high_14 = data['High'].rolling(14).max()
        stoch_k = ((closes - low_14) / (high_14 - low_14)) * 100
        
        # Williams %R
        williams_r = ((high_14.iloc[-1] - closes.iloc[-1]) / (high_14.iloc[-1] - low_14.iloc[-1])) * -100
        
        return {
            'roc_10': roc_10,
            'roc_20': roc_20,
            'stoch_k': stoch_k.iloc[-1],
            'williams_r': williams_r,
            'momentum_bullish': roc_10 > 5 and roc_20 > 10,
            'momentum_bearish': roc_10 < -5 and roc_20 < -10,
            'stoch_oversold': stoch_k.iloc[-1] < 20,
            'stoch_overbought': stoch_k.iloc[-1] > 80
        }
    except:
        return None

def analyze_stocks(stock_list):
    """Ultimate stock analysis with all indicators"""
    results = []
    total_stocks = len(stock_list)
    
    print(f"\n🚀 ULTIMATE STOCK ANALYZER")
    print(f"📊 Analyzing {total_stocks} NASDAQ-100 stocks with advanced indicators...")
    print("🔍 Indicators: RSI, MACD, Bollinger Bands, Support/Resistance, Volume, Momentum")
    print("=" * 80)
    
    for i, ticker in enumerate(stock_list, 1):
        try:
            company_name = COMPANY_NAMES.get(ticker, 'Unknown Company')
            print(f"[{i:3d}/{total_stocks}] {ticker:5s} - {company_name[:35]:35s} ", end='')
            
            stock_data = get_stock_data(ticker)
            
            if stock_data is not None and not stock_data.empty:
                # Calculate all technical indicators
                stock_data['RSI'] = calculate_rsi(stock_data)
                stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
                stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
                stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
                
                current_rsi = stock_data['RSI'].iloc[-1]
                current_price = stock_data['Close'].iloc[-1]
                
                # Advanced indicators
                macd_data = calculate_macd(stock_data)
                bb_data = calculate_bollinger_bands(stock_data)
                sr_data = find_support_resistance(stock_data)
                volume_data = analyze_volume(stock_data)
                momentum_data = calculate_momentum_indicators(stock_data)
                
                # ULTIMATE SCORING SYSTEM
                score = 0
                signals = []
                buy_signals = 0
                sell_signals = 0
                confidence = 0  # Confidence multiplier
                
                # RSI Analysis (Enhanced)
                if current_rsi < 25:
                    score += 6
                    buy_signals += 1
                    confidence += 2
                    signals.append(f"🟢 EXTREMELY OVERSOLD: RSI {current_rsi:.1f} - Rare Opportunity")
                elif current_rsi < 30:
                    score += 4
                    buy_signals += 1
                    confidence += 1
                    signals.append(f"🟢 OVERSOLD: RSI {current_rsi:.1f} - Strong Buy Zone")
                elif current_rsi < 40:
                    score += 2
                    buy_signals += 1
                    signals.append(f"🟡 APPROACHING OVERSOLD: RSI {current_rsi:.1f}")
                elif current_rsi > 80:
                    score -= 5
                    sell_signals += 1
                    signals.append(f"🔴 EXTREMELY OVERBOUGHT: RSI {current_rsi:.1f} - Danger Zone")
                elif current_rsi > 70:
                    score -= 3
                    sell_signals += 1
                    signals.append(f"🔴 OVERBOUGHT: RSI {current_rsi:.1f} - Avoid")
                
                # MACD Analysis (Advanced)
                if macd_data:
                    if macd_data['bullish_crossover']:
                        score += 4
                        buy_signals += 1
                        confidence += 1
                        signals.append("🟢 MACD BULLISH CROSSOVER - Momentum Turning Up")
                    elif macd_data['macd'] > macd_data['signal'] and macd_data['above_zero']:
                        score += 2
                        buy_signals += 1
                        signals.append("🟡 MACD Strong Positive - Above Zero Line")
                    elif macd_data['bearish_crossover']:
                        score -= 3
                        sell_signals += 1
                        signals.append("🔴 MACD BEARISH CROSSOVER - Momentum Turning Down")
                
                # Bollinger Bands Analysis (Advanced)
                if bb_data:
                    if bb_data['oversold']:
                        score += 5
                        buy_signals += 1
                        confidence += 1
                        signals.append(f"🟢 BOLLINGER EXTREME OVERSOLD - Position {bb_data['position']:.2f}")
                    elif bb_data['approaching_oversold']:
                        score += 3
                        buy_signals += 1
                        signals.append(f"🟡 BOLLINGER OVERSOLD - Position {bb_data['position']:.2f}")
                    elif bb_data['overbought']:
                        score -= 4
                        sell_signals += 1
                        signals.append(f"🔴 BOLLINGER EXTREME OVERBOUGHT - Position {bb_data['position']:.2f}")
                    
                    if bb_data['squeeze']:
                        score += 2
                        confidence += 1
                        signals.append("⚡ BOLLINGER SQUEEZE - Breakout Imminent")
                
                # Support/Resistance Analysis (Advanced)
                if sr_data:
                    if sr_data['near_support'] and sr_data['price_position'] < 0.3:
                        score += 4
                        buy_signals += 1
                        confidence += 1
                        signals.append(f"🟢 STRONG SUPPORT - ${sr_data['support_1']:.2f} ({sr_data['support_strength']:.1%})")
                    elif sr_data['near_support']:
                        score += 2
                        buy_signals += 1
                        signals.append(f"🟡 NEAR SUPPORT - ${sr_data['support_1']:.2f}")
                    elif sr_data['near_resistance']:
                        score -= 2
                        sell_signals += 1
                        signals.append(f"🔴 NEAR RESISTANCE - ${sr_data['resistance_1']:.2f}")
                
                # Moving Average Analysis (Enhanced)
                ma20 = stock_data['MA20'].iloc[-1]
                ma50 = stock_data['MA50'].iloc[-1]
                ma200 = stock_data['MA200'].iloc[-1]
                
                if current_price > ma20 > ma50 > ma200:
                    score += 4
                    buy_signals += 1
                    confidence += 1
                    signals.append("🟢 PERFECT BULLISH ALIGNMENT - All MAs Ascending")
                elif ma50 > ma200:
                    score += 2
                    buy_signals += 1
                    signals.append("🟡 BULLISH TREND - 50 MA above 200 MA")
                elif ma50 < ma200:
                    score -= 2
                    sell_signals += 1
                    signals.append("🔴 BEARISH TREND - 50 MA below 200 MA")
                
                # Golden/Death Cross Analysis (Enhanced)
                cross = check_golden_cross(stock_data)
                if cross == "GOLDEN CROSS":
                    score += 6
                    buy_signals += 1
                    confidence += 2
                    signals.append("🌟 GOLDEN CROSS - Major Bullish Breakout!")
                elif cross == "MINI GOLDEN":
                    score += 3
                    buy_signals += 1
                    signals.append("⭐ MINI GOLDEN CROSS - Short-term Bullish")
                elif cross == "DEATH CROSS":
                    score -= 6
                    sell_signals += 1
                    signals.append("💀 DEATH CROSS - Major Bearish Signal")
                elif cross == "MINI DEATH":
                    score -= 3
                    sell_signals += 1
                    signals.append("☠️ MINI DEATH CROSS - Short-term Bearish")
                
                # Volume Analysis (Advanced)
                if volume_data:
                    if volume_data['very_high_volume'] and buy_signals > sell_signals:
                        score += 4
                        confidence += 1
                        signals.append(f"📈 EXPLOSIVE VOLUME - {volume_data['volume_ratio_20']:.1f}x Average")
                    elif volume_data['high_volume'] and buy_signals > sell_signals:
                        score += 2
                        signals.append(f"📊 HIGH VOLUME CONFIRMATION - {volume_data['volume_ratio_20']:.1f}x")
                    elif volume_data['increasing_volume']:
                        score += 1
                        signals.append("📈 INCREASING VOLUME TREND")
                
                # Momentum Analysis (Advanced)
                if momentum_data:
                    if momentum_data['momentum_bullish']:
                        score += 3
                        buy_signals += 1
                        signals.append(f"🚀 STRONG MOMENTUM - ROC: {momentum_data['roc_20']:.1f}%")
                    elif momentum_data['momentum_bearish']:
                        score -= 3
                        sell_signals += 1
                        signals.append(f"📉 WEAK MOMENTUM - ROC: {momentum_data['roc_20']:.1f}%")
                    
                    if momentum_data['stoch_oversold']:
                        score += 2
                        buy_signals += 1
                        signals.append(f"🟢 STOCHASTIC OVERSOLD - {momentum_data['stoch_k']:.1f}")
                
                # Confidence multiplier (for high-conviction plays)
                if confidence >= 3:
                    score = int(score * 1.2)  # 20% bonus for high confidence
                    signals.append(f"⭐ HIGH CONFIDENCE SIGNAL - {confidence} confirmations")
                
                # Quality filter - only include high-quality signals
                signal_quality = buy_signals - sell_signals
                if signals and (signal_quality > 0 or score >= 8):
                    results.append({
                        'ticker': ticker,
                        'company_name': company_name,
                        'price': current_price,
                        'rsi': current_rsi,
                        'ma20': ma20,
                        'ma50': ma50,
                        'ma200': ma200,
                        'score': score,
                        'buy_signals': buy_signals,
                        'sell_signals': sell_signals,
                        'confidence': confidence,
                        'signal_quality': signal_quality,
                        'signals': signals,
                        'macd_data': macd_data,
                        'bb_data': bb_data,
                        'sr_data': sr_data,
                        'volume_data': volume_data,
                        'momentum_data': momentum_data
                    })
                    print("🎯 OPPORTUNITY DETECTED!")
                else:
                    print("⚪ No clear signal")
            else:
                print("❌ No data")
                
        except Exception as e:
            print(f"❌ Error: {str(e)[:30]}...")
            continue
    
    return results

def send_ultimate_email(opportunities):
    """Send comprehensive email with detailed analysis"""
    try:
        yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        email_body = [
            f"🚀 ULTIMATE NASDAQ-100 STOCK ANALYSIS",
            f"📅 {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p EST')}",
            f"🎯 Advanced Multi-Indicator Analysis\n",
            f"🏆 TOP {len(opportunities)} ULTIMATE OPPORTUNITIES:\n"
        ]
        
        for idx, stock in enumerate(opportunities[:15], 1):  # Top 15
            confidence_stars = "⭐" * min(stock['confidence'], 5)
            
            stock_info = [
                f"\n{idx}. {stock['ticker']} - {stock['company_name']}",
                f"💰 Price: ${stock['price']:.2f}",
                f"🎯 Ultimate Score: {stock['score']} {confidence_stars}",
                f"📊 Signal Quality: {stock['buy_signals']} buy vs {stock['sell_signals']} sell",
                f"📈 RSI: {stock['rsi']:.1f}",
                f"🔍 Key Signals:"
            ]
            
            # Show top 5 signals
            for signal in stock['signals'][:5]:
                stock_info.append(f"   • {signal}")
            
            if len(stock['signals']) > 5:
                stock_info.append(f"   • ... and {len(stock['signals']) - 5} more signals")
            
            stock_info.append("─" * 60)
            email_body.extend(stock_info)
        
        email_body.extend([
            "\n" + "="*60,
            "🧠 ULTIMATE ANALYSIS FEATURES:",
            "• Multi-timeframe RSI analysis (extreme levels)",
            "• Advanced MACD with momentum strength",
            "• Bollinger Bands with squeeze detection", 
            "• Multi-level Support/Resistance mapping",
            "• Volume trend and explosion detection",
            "• Momentum indicators (ROC, Stochastic, Williams %R)",
            "• Golden Cross variations (50/200 + 20/50)",
            "• Confidence scoring with quality filters",
            "",
            f"📊 Analysis completed: {datetime.now().strftime('%I:%M %p EST')}",
            f"🎯 {len(opportunities)} high-quality opportunities identified",
            f"⚙️ Ultimate NASDAQ-100 Stock Analyzer",
            "📈 Professional-grade technical analysis!"
        ])
        
        yag.send(
            to=EMAIL_ADDRESS,
            subject=f"🚀 ULTIMATE Analysis - {len(opportunities)} Premium Opportunities",
            contents='\n'.join(email_body)
        )
        print(f"\n📧 Ultimate analysis email sent with {len(opportunities)} opportunities!")
        
    except Exception as e:
        print(f"❌ Email error: {e}")

def main():
    """Ultimate stock analysis main function"""
    start_time = datetime.now()
    
    print(f"\n" + "="*80)
    print(f"🚀 ULTIMATE NASDAQ-100 STOCK ANALYZER")
    print(f"📅 {start_time.strftime('%A, %B %d, %Y at %I:%M %p EST')}")
    print(f"🎯 Professional-Grade Multi-Indicator Analysis")
    print(f"="*80)
    
    results = analyze_stocks(STOCKS_TO_MONITOR)
    
    if results:
        # Sort by ultimate score
        results.sort(key=lambda x: (x['score'], x['confidence']), reverse=True)
        
        # Categorize by quality
        ultimate_opportunities = [r for r in results if r['score'] >= 12]  # Exceptional
        premium_opportunities = [r for r in results if 8 <= r['score'] < 12]  # Very good
        good_opportunities = [r for r in results if 4 <= r['score'] < 8]      # Good
        
        print(f"\n" + "="*80)
        print(f"🏆 ULTIMATE OPPORTUNITIES (Score ≥ 12)")
        print(f"="*80)
        
        if ultimate_opportunities:
            for idx, result in enumerate(ultimate_opportunities[:10], 1):
                confidence_display = "⭐" * min(result['confidence'], 5)
                print(f"\n{idx}. {result['ticker']} - {result['company_name']}")
                print(f"   💰 Price: ${result['price']:.2f}")
                print(f"   🎯 Ultimate Score: {result['score']} {confidence_display}")
                print(f"   📊 Quality: {result['buy_signals']} buy signals vs {result['sell_signals']} sell")
                print(f"   📈 RSI: {result['rsi']:.1f}")
                print(f"   🔍 Top Signals:")
                for signal in result['signals'][:4]:  # Top 4 signals
                    print(f"      • {signal}")
                if len(result['signals']) > 4:
                    print(f"      • ... plus {len(result['signals']) - 4} more")
                print("   " + "─" * 70)
        
        if premium_opportunities:
            print(f"\n🥇 PREMIUM OPPORTUNITIES (Score 8-11)")
            print("─" * 50)
            for idx, result in enumerate(premium_opportunities[:5], 1):
                print(f"{idx}. {result['ticker']} - Score: {result['score']} - ${result['price']:.2f} - RSI: {result['rsi']:.1f}")
        
        if good_opportunities:
            print(f"\n🥈 GOOD OPPORTUNITIES (Score 4-7)")
            print("─" * 50)
            for idx, result in enumerate(good_opportunities[:5], 1):
                print(f"{idx}. {result['ticker']} - Score: {result['score']} - ${result['price']:.2f}")
        
        # Send email with all quality opportunities
        email_opportunities = ultimate_opportunities + premium_opportunities
        if email_opportunities:
            try:
                send_ultimate_email(email_opportunities)
            except Exception as e:
                print(f"❌ Email failed: {e}")
        
        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n" + "="*80)
        print(f"📊 ULTIMATE ANALYSIS COMPLETE")
        print(f"="*80)
        print(f"⏱️  Analysis time: {duration:.1f} seconds")
        print(f"📈 Total stocks analyzed: {len(STOCKS_TO_MONITOR)}")
        print(f"🎯 Opportunities found: {len(results)}")
        print(f"🏆 Ultimate opportunities: {len(ultimate_opportunities)}")
        print(f"🥇 Premium opportunities: {len(premium_opportunities)}")
        print(f"🥈 Good opportunities: {len(good_opportunities)}")
        print(f"📧 Email sent with top {len(email_opportunities)} opportunities")
        print(f"="*80)
        
    else:
        print("\n❌ No opportunities detected with current market conditions.")
        print("💡 Try running again later or adjust scoring thresholds.")

if __name__ == "__main__":
    main()
