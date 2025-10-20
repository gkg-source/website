import pandas as pd
import numpy as np
from scipy.stats import norm
import json
from datetime import datetime

class PortfolioOptimizer:
    def __init__(self):
        # Constants
        self.NUM_SIMULATIONS = 10000
        self.MIN_REAL_ESTATE_INVESTMENT = 1000000
        
        # Tax rates for different investment avenues
        self.tax_rates = {
            "Fixed Deposits": 0.30,
            "Government securities": 0.10,
            "Equity": 0.125,
            "Mutual Fund": 0.125,
            "Real Estate": 0.125,
            "Gold": 0.125
        }
        
        # Load investment data (you can modify this path)
        self.investment_data = self.load_investment_data()
    
    def load_investment_data(self):
        """Load investment metrics data - you can modify this to load from your CSV"""
        # Sample data structure - replace with your actual data loading
        sample_data = {
            "Fixed Deposits": {
                "cagr": 0.065,
                "volatility": 0.02,
                "beta": 0.0,
                "liquidity": 0.9
            },
            "Gold": {
                "cagr": 0.095,
                "volatility": 0.15,
                "beta": 0.3,
                "liquidity": 0.8
            },
            "Equity": {
                "cagr": 0.15,
                "volatility": 0.25,
                "beta": 1.0,
                "liquidity": 0.9
            },
            "Mutual Fund": {
                "cagr": 0.12,
                "volatility": 0.20,
                "beta": 0.8,
                "liquidity": 0.7
            },
            "Real Estate": {
                "cagr": 0.10,
                "volatility": 0.18,
                "beta": 0.5,
                "liquidity": 0.3
            },
            "Government securities": {
                "cagr": 0.07,
                "volatility": 0.08,
                "beta": 0.1,
                "liquidity": 0.6
            }
        }
        return sample_data
    
    def validate_inputs(self, inputs):
        """Validate user inputs"""
        emergency_fund = inputs["monthly_expenses"] * 6
        investable_amount = inputs["total_savings"] - emergency_fund
        
        if investable_amount < 0:
            raise ValueError(f"Insufficient savings. Need at least 6 months of expenses (₹{emergency_fund:,.2f}) as emergency fund.")
        
        if inputs["investment_amount"] > investable_amount:
            raise ValueError(f"Investment amount (₹{inputs['investment_amount']:,.2f}) exceeds the available investable amount (₹{investable_amount:,.2f}) after setting aside emergency fund.")
        
        if inputs["investment_amount"] <= 0:
            raise ValueError("Investment amount must be positive.")
        
        if inputs["financial_goal"] <= inputs["investment_amount"]:
            raise ValueError("Financial goal must be greater than the investment amount.")
        
        if inputs["investment_horizon"] <= 0:
            raise ValueError("Investment horizon must be at least 1 year.")
        
        return inputs
    
    def calculate_required_return(self, inputs):
        """Calculate required return to reach financial goal"""
        present_value = inputs["investment_amount"]
        future_value = inputs["financial_goal"]
        years = inputs["investment_horizon"]
        
        if present_value <= 0 or future_value <= 0 or years <= 0:
            return np.nan
        
        nominal_required_return = (future_value / present_value) ** (1 / years) - 1
        return nominal_required_return
    
    def allocate_assets(self, inputs):
        """Allocate assets based on risk tolerance and experience"""
        risk_tolerance = inputs["risk_tolerance"]
        experience = inputs["investment_experience"]
        liquidity_needs = inputs["liquidity_needs"]
        investment_amount = inputs["investment_amount"]
        
        # Initialize weights and selected assets
        weights = {
            "Fixed Deposits": 0,
            "Gold": 0,
            "Equity": 0,
            "Mutual Fund": 0,
            "Real Estate": 0,
            "Government securities": 0
        }
        
        selected_assets = {}
        
        # Risk tolerance-based allocation
        if risk_tolerance == "conservative":
            weights["Fixed Deposits"] = 0.40
            weights["Gold"] = 0.30
            remaining = 0.30
        elif risk_tolerance == "moderate":
            weights["Fixed Deposits"] = 0.10
            weights["Gold"] = 0.10
            remaining = 0.80
        else:  # aggressive
            weights["Fixed Deposits"] = 0.05
            weights["Gold"] = 0.05
            remaining = 0.90
        
        # Experience-based allocation
        risky_avenues = ["Equity", "Mutual Fund", "Government securities"]
        if investment_amount >= self.MIN_REAL_ESTATE_INVESTMENT:
            risky_avenues.append("Real Estate")
        
        if experience == "none":
            weights["Fixed Deposits"] += remaining / 2
            weights["Gold"] += remaining / 2
            remaining = 0
        elif experience == "intermediate":
            weights["Mutual Fund"] = remaining
            # Select appropriate mutual fund based on risk tolerance
            if risk_tolerance == "moderate":
                selected_assets["Mutual Fund"] = {"type": "Large Cap", "cagr": 0.12}
            else:  # aggressive
                selected_assets["Mutual Fund"] = {"type": "Mid Cap", "cagr": 0.15}
        else:  # advanced
            if investment_amount >= self.MIN_REAL_ESTATE_INVESTMENT:
                weights["Equity"] = remaining * 0.6
                weights["Mutual Fund"] = remaining * 0.3
                weights["Real Estate"] = remaining * 0.1
            else:
                weights["Equity"] = remaining * 0.7
                weights["Mutual Fund"] = remaining * 0.3
            
            # Select specific assets
            selected_assets["Equity"] = {"sector": "IT", "market_cap": "Large", "cagr": 0.18}
            selected_assets["Mutual Fund"] = {"type": "Multi Cap", "cagr": 0.14}
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            for avenue in weights:
                weights[avenue] /= total_weight
        
        return weights, selected_assets
    
    def calculate_portfolio_metrics(self, weights, inputs):
        """Calculate portfolio-level metrics"""
        portfolio_cagr = 0
        portfolio_volatility = 0
        portfolio_beta = 0
        
        for avenue, weight in weights.items():
            if weight > 0 and avenue in self.investment_data:
                asset_data = self.investment_data[avenue]
                portfolio_cagr += weight * asset_data["cagr"]
                portfolio_volatility += weight * asset_data["volatility"]
                portfolio_beta += weight * asset_data["beta"]
        
        # Tax-adjusted return
        tax_adj_cagr = 0
        for avenue, weight in weights.items():
            if weight > 0 and avenue in self.investment_data:
                asset_data = self.investment_data[avenue]
                tax_rate = self.tax_rates.get(avenue, inputs["tax_bracket"])
                tax_adj_cagr += weight * asset_data["cagr"] * (1 - tax_rate)
        
        real_return = tax_adj_cagr - inputs["expected_inflation"]
        
        return portfolio_cagr, tax_adj_cagr, real_return, portfolio_volatility, portfolio_beta
    
    def project_growth(self, inputs, portfolio_cagr_annual, real_return_annual):
        """Project portfolio growth over time"""
        amount = inputs["investment_amount"]
        years = inputs["investment_horizon"]
        
        portfolio_cagr_annual = portfolio_cagr_annual if np.isfinite(portfolio_cagr_annual) else 0
        real_return_annual = real_return_annual if np.isfinite(real_return_annual) else 0
        
        nominal_rate_decimal = portfolio_cagr_annual
        real_rate_decimal = real_return_annual
        
        if nominal_rate_decimal <= -1:
            nominal_value = 0
        else:
            nominal_value = amount * (1 + nominal_rate_decimal) ** years
        
        if real_rate_decimal <= -1:
            real_value = 0
        else:
            real_value = amount * (1 + real_rate_decimal) ** years
        
        return nominal_value, real_value
    
    def monte_carlo_simulation(self, inputs, portfolio_cagr, portfolio_volatility):
        """Run Monte Carlo simulation for portfolio projections"""
        years = inputs["investment_horizon"]
        amount = inputs["investment_amount"]
        
        sim_cagr = portfolio_cagr if np.isfinite(portfolio_cagr) else 0
        sim_volatility = portfolio_volatility if np.isfinite(portfolio_volatility) else 0
        
        if sim_volatility <= 0:
            final_value = amount * (1 + sim_cagr) ** years
            return final_value, final_value, final_value
        
        final_values = []
        for _ in range(self.NUM_SIMULATIONS):
            annual_returns = norm.rvs(loc=sim_cagr, scale=sim_volatility, size=years)
            annual_returns = np.maximum(annual_returns, -0.99)
            final_value = amount * np.prod(1 + annual_returns)
            final_values.append(final_value)
        
        final_values = np.array(final_values)
        final_values = final_values[np.isfinite(final_values)]
        
        if len(final_values) == 0:
            return np.nan, np.nan, np.nan
        
        mean_value = np.mean(final_values)
        percentile_5 = np.percentile(final_values, 5)
        percentile_95 = np.percentile(final_values, 95)
        
        return mean_value, percentile_5, percentile_95
    
    def stress_test(self, weights):
        """Run stress test for portfolio"""
        stress_impacts = {
            "Fixed Deposits": 0.00,
            "Government securities": 0.05,
            "Equity": 0.30,
            "Mutual Fund": 0.25,
            "Real Estate": 0.20,
            "Gold": 0.10
        }
        
        portfolio_drop_pct = 0
        for avenue, weight in weights.items():
            if weight > 0 and avenue in stress_impacts:
                portfolio_drop_pct += weight * stress_impacts[avenue]
        
        return portfolio_drop_pct * 100
    
    def optimize_portfolio(self, user_inputs):
        """Main portfolio optimization function"""
        try:
            # Validate inputs
            validated_inputs = self.validate_inputs(user_inputs)
            
            # Calculate required return
            required_return = self.calculate_required_return(validated_inputs)
            
            # Allocate assets
            weights, selected_assets = self.allocate_assets(validated_inputs)
            
            # Calculate portfolio metrics
            portfolio_cagr, tax_adj_cagr, real_return, volatility, beta = self.calculate_portfolio_metrics(weights, validated_inputs)
            
            # Project growth
            nominal_value, real_value = self.project_growth(validated_inputs, portfolio_cagr, real_return)
            
            # Run Monte Carlo simulation
            mean_value, p5, p95 = self.monte_carlo_simulation(validated_inputs, portfolio_cagr, volatility)
            
            # Run stress test
            crash_impact = self.stress_test(weights)
            
            # Prepare results
            results = {
                'required_return_percent': required_return * 100 if np.isfinite(required_return) else None,
                'asset_allocation': {k: v * 100 for k, v in weights.items() if v > 0},
                'selected_assets': selected_assets,
                'portfolio_cagr_percent': portfolio_cagr * 100 if np.isfinite(portfolio_cagr) else None,
                'tax_adj_cagr_percent': tax_adj_cagr * 100 if np.isfinite(tax_adj_cagr) else None,
                'real_return_percent': real_return * 100 if np.isfinite(real_return) else None,
                'portfolio_volatility_percent': volatility * 100 if np.isfinite(volatility) else None,
                'portfolio_beta': beta if np.isfinite(beta) else None,
                'projected_nominal_value': nominal_value if np.isfinite(nominal_value) else None,
                'projected_real_value': real_value if np.isfinite(real_value) else None,
                'monte_carlo_results': {
                    'mean_value': mean_value if np.isfinite(mean_value) else None,
                    'percentile_5': p5 if np.isfinite(p5) else None,
                    'percentile_95': p95 if np.isfinite(p95) else None
                },
                'stress_test_percent': crash_impact if np.isfinite(crash_impact) else None,
                'recommendations': self.generate_recommendations(weights, portfolio_cagr, required_return)
            }
            
            return results
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_recommendations(self, weights, portfolio_cagr, required_return):
        """Generate personalized recommendations"""
        recommendations = []
        
        if portfolio_cagr < required_return:
            recommendations.append("Your current portfolio allocation may not meet your financial goals. Consider increasing exposure to higher-return assets.")
        
        if weights.get("Equity", 0) > 0.7:
            recommendations.append("High equity exposure detected. Consider diversifying with fixed income for stability.")
        
        if weights.get("Fixed Deposits", 0) > 0.5:
            recommendations.append("High fixed deposit allocation. Consider diversifying for better returns while maintaining safety.")
        
        if not recommendations:
            recommendations.append("Your portfolio allocation looks well-balanced for your risk profile and goals.")
        
        return recommendations

# Example usage
if __name__ == "__main__":
    optimizer = PortfolioOptimizer()
    
    # Sample user inputs
    user_inputs = {
        "age": 30,
        "annual_income": 1000000,
        "total_savings": 750000,
        "monthly_expenses": 30000,
        "investment_amount": 500000,
        "investment_horizon": 10,
        "risk_tolerance": "moderate",
        "financial_goal": 1000000,
        "investment_experience": "intermediate",
        "liquidity_needs": "moderate",
        "tax_bracket": 0.125,
        "expected_inflation": 0.06
    }
    
    # Optimize portfolio
    results = optimizer.optimize_portfolio(user_inputs)
    
    if 'error' not in results:
        print("Portfolio Optimization Results:")
        print(f"Required Return: {results['required_return_percent']:.2f}%")
        print(f"Expected Portfolio CAGR: {results['portfolio_cagr_percent']:.2f}%")
        print(f"Real Return: {results['real_return_percent']:.2f}%")
        print(f"Portfolio Volatility: {results['portfolio_volatility_percent']:.2f}%")
        
        print("\nAsset Allocation:")
        for asset, allocation in results['asset_allocation'].items():
            print(f"{asset}: {allocation:.1f}%")
        
        print(f"\nProjected Value (10 years): ₹{results['projected_nominal_value']:,.2f}")
        print(f"Stress Test Impact: {results['stress_test_percent']:.1f}%")
        
        print("\nRecommendations:")
        for rec in results['recommendations']:
            print(f"- {rec}")
    else:
        print(f"Error: {results['error']}")

