import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta

class BudgetOptimizer:
    def __init__(self, monthly_income, irregular_income=0, irregular_freq="monthly", 
                 outstanding_loans=0, emi=0, food_input=0, leisure_input=0, 
                 travel_input=0, fixed_costs=0, savings_input=0, monthly_savings_goal=0,
                 goal="Save More", extra_emi=0, interest_rate=0, loan_tenure=0, 
                 financial_goal_amount=0, months_to_goal=0):
        
        self.monthly_income = monthly_income
        self.monthly_irregular = irregular_income / 3 if irregular_freq == "quarterly" else irregular_income / 12 if irregular_freq == "yearly" else irregular_income
        self.income = self.monthly_income + self.monthly_irregular
        self.outstanding_loans = outstanding_loans
        self.emi = emi
        self.food_input = food_input
        self.leisure_input = leisure_input
        self.travel_input = travel_input
        self.fixed_costs = fixed_costs
        self.savings_input = savings_input
        self.monthly_savings_goal = monthly_savings_goal
        self.food = self.food_input
        self.leisure = self.leisure_input
        self.travel = self.travel_input
        self.discretionary = self.food + self.leisure + self.travel
        self.savings = self.savings_input
        self.debt = self.emi
        self.goal = goal
        self.financial_goal_amount = financial_goal_amount
        self.months_to_goal = months_to_goal
        self.extra_emi = extra_emi if goal == "Debt Freedom" else 0
        self.interest_rate = interest_rate / 100 if interest_rate else None
        self.loan_tenure = loan_tenure
        self.optimized_budget = {}
        
    def calculate_loan_tenure(self, emi, principal, rate):
        """Calculate loan tenure given EMI, principal, and interest rate"""
        monthly_rate = rate / 12
        if monthly_rate == 0:
            return principal / emi if emi > 0 else float('inf')
        n = np.log(1 - (principal * monthly_rate) / emi) / np.log(1 + monthly_rate)
        return max(0, -n) if n < 0 else n
    
    def loan_amortization(self, emi, principal, rate):
        """Calculate loan amortization schedule"""
        monthly_rate = rate / 12
        balance = principal
        months = []
        balances = []
        month = 0
        while balance > 0 and month < 1000:
            interest = balance * monthly_rate
            principal_payment = emi - interest
            balance = max(0, balance - principal_payment)
            months.append(month)
            balances.append(balance)
            month += 1
        return months, balances
    
    def apply_save_more_rule(self):
        """Apply 50/30/20 rule for saving more"""
        target_savings = max(self.monthly_savings_goal, self.income * 0.20)
        shortfall = target_savings - self.savings
        
        if shortfall > 0:
            # Reduce discretionary spending if it's high
            if self.leisure > self.income * 0.15:
                reduction = self.leisure * 0.20
                self.leisure -= reduction
                self.savings += reduction
                shortfall -= reduction
            
            if self.food > self.income * 0.20 and shortfall > 0:
                reduction = self.food * 0.20
                self.food -= reduction
                self.savings += reduction
                shortfall -= reduction
            
            if self.travel > self.income * 0.10 and shortfall > 0:
                reduction = self.travel * 0.20
                self.travel -= reduction
                self.savings += reduction
        
        # Ensure fixed costs don't exceed 50% of income
        if self.fixed_costs > self.income * 0.50:
            print("Warning: Fixed costs exceed 50% of income. Consider reducing essentials.")
        
        self.optimized_budget = {
            'Fixed Costs': self.fixed_costs,
            'Food': self.food,
            'Travel': self.travel,
            'Leisure': self.leisure,
            'Savings': self.savings,
            'Debt Payment': self.debt
        }
    
    def apply_debt_freedom_rule(self):
        """Optimize for debt freedom"""
        debt_ratio = self.outstanding_loans / self.income
        target_debt_payment = self.income * 0.20  # Minimum 20%
        
        if debt_ratio > 0.20:
            target_debt_payment = self.income * 0.30  # 30% for high debt
            # Reduce discretionary spending
            self.leisure *= 0.80
            self.food *= 0.80
            self.travel *= 0.80
        
        # Add extra EMI if specified
        total_debt_payment = target_debt_payment + self.extra_emi
        
        # Ensure minimum savings
        self.savings = max(self.income * 0.10, self.savings)
        
        self.optimized_budget = {
            'Fixed Costs': self.fixed_costs,
            'Food': self.food,
            'Travel': self.travel,
            'Leisure': self.leisure,
            'Savings': self.savings,
            'Debt Payment': total_debt_payment
        }
    
    def apply_investment_focus_rule(self):
        """Optimize for investment focus"""
        # Target 30% savings for investments
        target_savings = max(self.monthly_savings_goal, self.income * 0.30)
        shortfall = target_savings - self.savings
        
        if shortfall > 0:
            # Reduce discretionary spending proportionally
            total_discretionary = self.food + self.leisure + self.travel
            if total_discretionary > 0:
                reduction_ratio = shortfall / total_discretionary
                self.food *= (1 - reduction_ratio * 0.4)  # Food gets 40% of reduction
                self.leisure *= (1 - reduction_ratio * 0.4)  # Leisure gets 40% of reduction
                self.travel *= (1 - reduction_ratio * 0.2)  # Travel gets 20% of reduction
                self.savings = target_savings
        
        self.optimized_budget = {
            'Fixed Costs': self.fixed_costs,
            'Food': self.food,
            'Travel': self.travel,
            'Leisure': self.leisure,
            'Savings': self.savings,
            'Debt Payment': self.debt
        }
    
    def optimize_budget(self):
        """Main optimization function"""
        if self.goal == "Save More":
            self.apply_save_more_rule()
        elif self.goal == "Debt Freedom":
            self.apply_debt_freedom_rule()
        elif self.goal == "Investment Focus":
            self.apply_investment_focus_rule()
        else:
            # Default to balanced approach
            self.apply_save_more_rule()
        
        return self.optimized_budget
    
    def get_budget_analysis(self):
        """Get comprehensive budget analysis"""
        total_expenses = sum(self.optimized_budget.values())
        savings_rate = (self.savings / self.income) * 100
        debt_ratio = (self.debt / self.income) * 100
        discretionary_ratio = ((self.food + self.leisure + self.travel) / self.income) * 100
        
        analysis = {
            'total_income': self.income,
            'total_expenses': total_expenses,
            'net_savings': self.income - total_expenses,
            'savings_rate_percent': savings_rate,
            'debt_ratio_percent': debt_ratio,
            'discretionary_ratio_percent': discretionary_ratio,
            'budget_breakdown': self.optimized_budget,
            'recommendations': self.get_recommendations()
        }
        
        return analysis
    
    def get_recommendations(self):
        """Get personalized budget recommendations"""
        recommendations = []
        
        if self.fixed_costs > self.income * 0.50:
            recommendations.append("Fixed costs are too high. Consider reducing rent, utilities, or insurance costs.")
        
        if self.savings < self.income * 0.20:
            recommendations.append("Aim to save at least 20% of your income for financial security.")
        
        if self.debt > self.income * 0.30:
            recommendations.append("Debt payments are high. Consider debt consolidation or refinancing.")
        
        if self.leisure > self.income * 0.25:
            recommendations.append("Leisure spending is high. Consider reducing entertainment expenses.")
        
        if self.food > self.income * 0.25:
            recommendations.append("Food spending is high. Consider meal planning and cooking at home.")
        
        if not recommendations:
            recommendations.append("Your budget looks well-balanced! Keep up the good work.")
        
        return recommendations
    
    def calculate_financial_goal_progress(self):
        """Calculate progress towards financial goal"""
        if self.financial_goal_amount <= 0 or self.months_to_goal <= 0:
            return None
        
        monthly_required = self.financial_goal_amount / self.months_to_goal
        current_savings = self.savings
        
        if current_savings >= monthly_required:
            status = "On Track"
            months_ahead = int((current_savings - monthly_required) / monthly_required)
        else:
            status = "Behind Schedule"
            months_behind = int((monthly_required - current_savings) / monthly_required)
        
        return {
            'monthly_required': monthly_required,
            'current_savings': current_savings,
            'status': status,
            'progress_percent': min(100, (current_savings / monthly_required) * 100)
        }
    
    def export_budget_report(self, format_type="json"):
        """Export budget report in various formats"""
        analysis = self.get_budget_analysis()
        
        if format_type == "json":
            return json.dumps(analysis, indent=2)
        elif format_type == "dict":
            return analysis
        else:
            return str(analysis)

# Example usage
if __name__ == "__main__":
    # Create budget optimizer instance
    optimizer = BudgetOptimizer(
        monthly_income=50000,
        irregular_income=10000,
        irregular_freq="quarterly",
        outstanding_loans=200000,
        emi=5000,
        food_input=8000,
        leisure_input=6000,
        travel_input=3000,
        fixed_costs=15000,
        savings_input=5000,
        monthly_savings_goal=10000,
        goal="Save More"
    )
    
    # Optimize budget
    optimized = optimizer.optimize_budget()
    print("Optimized Budget:")
    for category, amount in optimized.items():
        print(f"{category}: ₹{amount:,.2f}")
    
    # Get analysis
    analysis = optimizer.get_budget_analysis()
    print(f"\nSavings Rate: {analysis['savings_rate_percent']:.1f}%")
    print(f"Debt Ratio: {analysis['debt_ratio_percent']:.1f}%")
    
    # Get recommendations
    print("\nRecommendations:")
    for rec in analysis['recommendations']:
        print(f"- {rec}")

