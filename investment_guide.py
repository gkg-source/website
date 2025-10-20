import pandas as pd
import numpy as np
from scipy.stats import norm
import yfinance as yf
from datetime import datetime, timedelta
import json

class InvestmentGuide:
    def __init__(self):
        # Parameters (2025, India)
        self.risk_free_rate = 6.25 / 100  # 10-Year G-Sec yield
        self.inflation_rate = 5.5 / 100  # CPI projection
        self.tax_rate = 0.125  # Long-term capital gains tax
        self.market_risk_premium = 7.5 / 100  # NIFTY 50 premium
        
    def analyze_fixed_deposits(self):
        """Analyze Fixed Deposits with inflation and tax adjustments"""
        data = {
            'Date': ['2020-2022', '2022-2023', '2023-2024', '2024-2025'],
            '1_year': [5.5, 6.6, 6.9, 6.9],
            '2_year': [5.5, 6.8, 7.0, 7.0],
            '3_year': [5.5, 6.9, 7.0, 7.1],
            '5_year': [6.7, 7.0, 7.5, 7.5]
        }
        
        df = pd.DataFrame(data)
        
        # Convert Date to numeric years
        def parse_year(date_str):
            if '-' in date_str:
                start, end = map(int, date_str.split('-'))
                return (start + end) / 2
            return int(date_str)
        
        df['Year'] = df['Date'].apply(parse_year)
        df = df.drop('Date', axis=1)
        
        # Function to calculate CAGR from yearly rates
        def calculate_cagr(rates, years):
            if len(rates) == 0:
                return np.nan
            cumulative_return = 1.0
            for rate in rates:
                cumulative_return *= (1 + rate / 100)
            return (cumulative_return ** (1 / years) - 1) if years > 0 else np.nan
        
        # Calculate metrics
        results = []
        tenures = ['1_year', '2_year', '3_year', '5_year']
        subcategories = ['1-Year', '2-Year', '3-Year', '5-Year']
        
        for tenure, subcategory in zip(tenures, subcategories):
            rates = df[tenure].values
            years = len(rates)
            
            # CAGR (historical, 2020–2025)
            cagr = calculate_cagr(rates, years)
            
            # Volatility (based on yearly rate changes, minimal for FDs)
            rate_changes = np.diff(rates) / 100
            volatility = np.std(rate_changes) * np.sqrt(252) if len(rate_changes) > 0 else 0.0
            
            # Sharpe Ratio
            sharpe_ratio = np.nan if volatility == 0 else (cagr - self.risk_free_rate) / volatility
            
            # Beta (FDs are non-market-correlated)
            beta = 0.0
            
            # CAPM Expected Return
            capm_return = self.risk_free_rate + beta * self.market_risk_premium
            
            # Real Return
            post_tax_return = cagr * (1 - 0.30)  # 30% tax for FDs
            real_return = post_tax_return - self.inflation_rate
            
            # Liquidity (assumed, shorter tenures more liquid)
            liquidity_scores = {'1_year': 0.05, '2_year': 0.03, '3_year': 0.02, '5_year': 0.01}
            min_volume = 50000
            max_volume = 5000000
            liquidity_range = max_volume - min_volume
            liquidity_level = (liquidity_scores[tenure] * max_volume - min_volume) / liquidity_range
            liquidity_level = max(0, min(1, liquidity_level))
            
            # Risk Level
            risk_level = 'Low' if volatility < 0.20 else 'Medium' if volatility < 0.30 else 'High'
            
            results.append({
                'Subcategory': subcategory,
                'CAGR (%)': cagr * 100,
                'Volatility (%)': volatility * 100,
                'Sharpe_Ratio': sharpe_ratio,
                'Beta': beta,
                'CAPM_Expected_Return (%)': capm_return * 100,
                'Real_Return (%)': real_return * 100,
                'Risk_Level': risk_level,
                'Liquidity_Level': liquidity_level,
                'Investment_Avenue': 'Fixed Deposits'
            })
        
        return pd.DataFrame(results)
    
    def analyze_equity(self, start_date=None, end_date=None):
        """Analyze equity markets across sectors and market caps"""
        if start_date is None:
            start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            
        # Define sectors and representative stocks
        sectors = {
            'IT': {
                'Large': ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS'],
                'Mid': ['TATAELXSI.NS', 'KPITTECH.NS', 'CYIENT.NS', 'SONATSOFTW.NS'],
                'Small': ['QUICKHEAL.NS', 'SAKSOFT.NS', 'XCHANGING.NS', 'RSSOFTWARE.NS']
            },
            'Banking': {
                'Large': ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'KOTAKBANK.NS', 'AXISBANK.NS'],
                'Mid': ['FEDERALBNK.NS', 'RBLBANK.NS', 'IDFCFIRSTB.NS', 'BANDHANBNK.NS'],
                'Small': ['SURYODAY.NS', 'EQUITASBNK.NS', 'CSBBANK.NS', 'UTKARSHBNK.NS']
            },
            'Pharma': {
                'Large': ['SUNPHARMA.NS', 'DIVISLAB.NS', 'CIPLA.NS', 'DRREDDY.NS', 'ZYDUSLIFE.NS'],
                'Mid': ['GLENMARK.NS', 'IPCALAB.NS', 'NATCOPHARM.NS', 'AJANTPHARM.NS'],
                'Small': ['LINCOLN.NS', 'KOPRAN.NS', 'WANBURY.NS', 'BALPHARMA.NS']
            },
            'Auto': {
                'Large': ['MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'EICHERMOT.NS'],
                'Mid': ['SONACOMS.NS', 'ENDURANCE.NS', 'MINDACORP.NS', 'SUNDRMFAST.NS'],
                'Small': ['FIEMIND.NS', 'SSWL.NS', 'AUTOIND.NS', 'MUNJALSHOW.NS']
            },
            'Energy': {
                'Large': ['RELIANCE.NS', 'ONGC.NS', 'NTPC.NS', 'POWERGRID.NS', 'BPCL.NS'],
                'Mid': ['TATAPOWER.NS', 'JSWENERGY.NS', 'TORNTPOWER.NS', 'CESC.NS'],
                'Small': ['GIPCL.NS', 'BFUTILITIE.NS', 'JPPOWER.NS', 'RPOWER.NS']
            }
        }
        
        # Fetch market data for beta calculation
        market_ticker = '^NSEI'
        try:
            market_data = yf.Ticker(market_ticker).history(start=start_date, end=end_date)
            if market_data.empty or len(market_data) < 252:
                raise ValueError("Insufficient market data for NIFTY 50")
            market_daily_returns = market_data['Close'].pct_change().dropna()
            market_daily_returns.index = market_daily_returns.index.tz_localize(None)
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return pd.DataFrame()
        
        def analyze_stock(ticker):
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(start=start_date, end=end_date)
                
                if hist.empty or len(hist) < 252:
                    return None
                
                hist.index = hist.index.tz_localize(None)
                
                # CAGR
                start_price = hist['Close'].iloc[0]
                end_price = hist['Close'].iloc[-1]
                years = (hist.index[-1] - hist.index[0]).days / 365.25
                cagr = (end_price / start_price) ** (1.0 / years) - 1
                
                # Daily returns
                daily_returns = hist['Close'].pct_change().dropna()
                if len(daily_returns) < 100:
                    return None
                
                # Volatility (annualized)
                volatility = daily_returns.std() * np.sqrt(252)
                
                # Sharpe Ratio (annualized)
                excess_return = cagr - self.risk_free_rate
                sharpe_ratio = excess_return / volatility if volatility != 0 else np.nan
                
                # Beta (relative to NIFTY 50)
                aligned_returns = pd.concat([daily_returns, market_daily_returns], axis=1).dropna()
                if len(aligned_returns) < 50:
                    return None
                stock_returns = aligned_returns.iloc[:, 0]
                market_returns = aligned_returns.iloc[:, 1]
                cov = stock_returns.cov(market_returns)
                market_var = market_returns.var()
                beta = cov / market_var if market_var != 0 else np.nan
                
                # CAPM Expected Return
                capm_return = self.risk_free_rate + beta * self.market_risk_premium if not np.isnan(beta) else np.nan
                
                # Real Return (post-tax, inflation-adjusted)
                post_tax_return = cagr * (1 - self.tax_rate)
                real_return = post_tax_return - self.inflation_rate
                
                # Liquidity (average daily volume)
                avg_volume = hist['Volume'].mean()
                
                # Risk Level
                risk_level = 'Low' if volatility < 0.20 else 'Medium' if volatility < 0.30 else 'High'
                
                return {
                    'CAGR': cagr,
                    'Volatility': volatility,
                    'Sharpe_Ratio': sharpe_ratio,
                    'Beta': beta,
                    'CAPM_Expected_Return': capm_return,
                    'Real_Return': real_return,
                    'Liquidity': avg_volume,
                    'Risk_Level': risk_level
                }
            except Exception as e:
                return None
        
        # Analyze all stocks
        results = []
        for sector, caps in sectors.items():
            for cap, tickers in caps.items():
                for ticker in tickers:
                    result = analyze_stock(ticker)
                    if result:
                        results.append({
                            'Sector': sector,
                            'Cap': cap,
                            'Ticker': ticker,
                            **result
                        })
        
        if not results:
            return pd.DataFrame()
        
        # Create DataFrame and aggregate
        df = pd.DataFrame(results)
        agg_df = df.groupby(['Sector', 'Cap']).agg({
            'CAGR': 'mean',
            'Volatility': 'mean',
            'Sharpe_Ratio': 'mean',
            'Beta': 'mean',
            'CAPM_Expected_Return': 'mean',
            'Real_Return': 'mean',
            'Liquidity': 'mean',
            'Risk_Level': lambda x: x.mode()[0] if not x.empty else 'Unknown'
        }).reset_index()
        
        # Normalize Liquidity Level (0-1 scale)
        agg_df['Liquidity_Level'] = (agg_df['Liquidity'] - agg_df['Liquidity'].min()) / (agg_df['Liquidity'].max() - agg_df['Liquidity'].min())
        agg_df = agg_df.drop(columns=['Liquidity'])
        
        # Convert to percentages for display
        agg_df['CAGR'] *= 100
        agg_df['Volatility'] *= 100
        agg_df['CAPM_Expected_Return'] *= 100
        agg_df['Real_Return'] *= 100
        
        # Rename columns
        agg_df.columns = [
            'Sector', 'Cap', 'CAGR (%)', 'Volatility (%)', 'Sharpe_Ratio', 'Beta',
            'CAPM_Expected_Return (%)', 'Real_Return (%)', 'Risk_Level', 'Liquidity_Level'
        ]
        
        return agg_df
    
    def get_investment_recommendations(self, user_profile):
        """Get personalized investment recommendations based on user profile"""
        recommendations = {
            'conservative': {
                'Fixed Deposits': 0.40,
                'Gold': 0.30,
                'Government Securities': 0.20,
                'Mutual Funds (Large Cap)': 0.10
            },
            'moderate': {
                'Fixed Deposits': 0.20,
                'Gold': 0.20,
                'Mutual Funds (Large Cap)': 0.40,
                'Equity (Large Cap)': 0.20
            },
            'aggressive': {
                'Fixed Deposits': 0.10,
                'Gold': 0.10,
                'Equity (Mid/Small Cap)': 0.50,
                'Mutual Funds (Mid Cap)': 0.30
            }
        }
        
        risk_tolerance = user_profile.get('risk_tolerance', 'moderate')
        return recommendations.get(risk_tolerance, recommendations['moderate'])
    
    def calculate_portfolio_metrics(self, weights, investment_data):
        """Calculate portfolio-level metrics"""
        portfolio_cagr = 0
        portfolio_volatility = 0
        portfolio_beta = 0
        
        for asset, weight in weights.items():
            if weight > 0 and asset in investment_data:
                asset_data = investment_data[asset]
                portfolio_cagr += weight * asset_data.get('cagr', 0)
                portfolio_volatility += weight * asset_data.get('volatility', 0)
                portfolio_beta += weight * asset_data.get('beta', 0)
        
        return {
            'portfolio_cagr': portfolio_cagr,
            'portfolio_volatility': portfolio_volatility,
            'portfolio_beta': portfolio_beta
        }

# Example usage
if __name__ == "__main__":
    guide = InvestmentGuide()
    
    # Analyze Fixed Deposits
    fd_results = guide.analyze_fixed_deposits()
    print("Fixed Deposits Analysis:")
    print(fd_results)
    
    # Analyze Equity (commented out to avoid API calls during testing)
    # equity_results = guide.analyze_equity()
    # print("\nEquity Analysis:")
    # print(equity_results)
    
    # Get recommendations
    user_profile = {'risk_tolerance': 'moderate'}
    recommendations = guide.get_investment_recommendations(user_profile)
    print("\nInvestment Recommendations:")
    for asset, allocation in recommendations.items():
        print(f"{asset}: {allocation*100:.1f}%")

