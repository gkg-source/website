from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
import os
import datetime
import bcrypt
import jwt
import requests
import math
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our financial tools (with fallback for missing modules)
try:
    from investment_guide import InvestmentGuide
except ImportError:
    InvestmentGuide = None
    print("⚠️ investment_guide module not found, some features may be limited")

try:
    from budget_optimizer import BudgetOptimizer
except ImportError:
    BudgetOptimizer = None
    print("⚠️ budget_optimizer module not found, some features may be limited")

try:
    from portfolio_optimizer import PortfolioOptimizer
except ImportError:
    PortfolioOptimizer = None
    print("⚠️ portfolio_optimizer module not found, some features may be limited")

app = Flask(__name__)

# CORS configuration for production
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

# JWT configuration
JWT_SECRET = os.environ.get('JWT_SECRET', 'change-this-in-production')
JWT_ALG = 'HS256'
JWT_EXPIRE_MINUTES = 60 * 24

# Simple JSON storage for demo users
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_user_by_email(users, email):
    email_lower = (email or '').strip().lower()
    return users.get(email_lower)


def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password, password_hash):
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False


def generate_token(user_payload):
    now = datetime.datetime.utcnow()
    exp = now + datetime.timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {
        'sub': user_payload['email'],
        'name': user_payload.get('name'),
        'email': user_payload.get('email'),
        'phone': user_payload.get('phone'),
        'profile': user_payload.get('profile', {}),
        'iat': now,
        'exp': exp,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])


# JWT Authentication Decorator
from functools import wraps

def jwt_required(f):
    """Decorator to require JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Format: "Bearer <token>"
                token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            except IndexError:
                return jsonify({'success': False, 'error': 'Invalid authorization header format'}), 401
        
        # If no token in header, try to get from request body
        if not token:
            data = request.get_json(silent=True) or {}
            token = data.get('token') or data.get('authToken')
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        try:
            # Decode and verify token
            payload = decode_token(token)
            users = load_users()
            user = get_user_by_email(users, payload.get('email'))
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 401
            
            # Create current_user object
            current_user = {
                'email': user.get('email'),
                'name': user.get('name'),
                'phone': user.get('phone'),
                'profile': user.get('profile', {})
            }
            
            # Call the original function with current_user
            return f(current_user=current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'success': False, 'error': f'Authentication failed: {str(e)}'}), 401
    
    return decorated_function

# Initialize our tools (with fallback if modules don't exist)
investment_guide = InvestmentGuide() if InvestmentGuide else None
portfolio_optimizer = PortfolioOptimizer() if PortfolioOptimizer else None

@app.route('/')
def home():
    return jsonify({
        "message": "Ghar Ka Guide Financial API",
        "endpoints": {
            "investment_analysis": "/api/investment/analyze",
            "budget_optimization": "/api/budget/optimize",
            "portfolio_optimization": "/api/portfolio/optimize",
            "investment_recommendations": "/api/investment/recommendations",
            "auth_signup": "/api/auth/signup",
            "auth_login": "/api/auth/login",
            "auth_verify": "/api/auth/verify",
            "auth_profile": "/api/auth/profile",
            "auth_logout": "/api/auth/logout"
        }
    })


# Auth: signup
@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    try:
        data = request.get_json(force=True) or {}
        name = (data.get('name') or '').strip()
        email = (data.get('email') or '').strip().lower()
        phone = (data.get('phone') or '').strip()
        password = data.get('password') or ''

        if not name or not email or not password:
            return jsonify({'success': False, 'error': 'name, email, and password are required'}), 400

        users = load_users()
        if get_user_by_email(users, email):
            return jsonify({'success': False, 'error': 'Email already registered'}), 400

        user_record = {
            'name': name,
            'email': email,
            'phone': phone,
            'password_hash': hash_password(password),
            'profile': {
                'age': data.get('age', 30),
                'income': data.get('income', 500000),
                'risk_tolerance': data.get('risk_tolerance', 'moderate'),
                'investment_experience': data.get('investment_experience', 'beginner')
            }
        }
        users[email] = user_record
        save_users(users)

        public_user = {k: v for k, v in user_record.items() if k != 'password_hash'}
        return jsonify({'success': True, 'user': public_user})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Auth: login
@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    try:
        data = request.get_json(force=True) or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''

        users = load_users()
        user = get_user_by_email(users, email)
        if not user or not verify_password(password, user.get('password_hash', '')):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        token = generate_token(user)
        public_user = {k: v for k, v in user.items() if k != 'password_hash'}
        return jsonify({'success': True, 'token': token, 'user': public_user})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Auth: verify
@app.route('/api/auth/verify', methods=['POST'])
def auth_verify():
    try:
        data = request.get_json(force=True) or {}
        token = (data.get('token') or '').strip()
        if not token:
            return jsonify({'success': False, 'error': 'Token required'}), 400

        payload = decode_token(token)
        users = load_users()
        user = get_user_by_email(users, payload.get('email'))
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401

        public_user = {k: v for k, v in user.items() if k != 'password_hash'}
        return jsonify({'success': True, 'user': public_user})
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Auth: profile update
@app.route('/api/auth/profile', methods=['PUT'])
def auth_profile():
    try:
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer', '').strip() if auth_header else ''
        if not token:
            return jsonify({'success': False, 'error': 'Authorization token required'}), 401

        payload = decode_token(token)
        email = (payload.get('email') or '').strip().lower()

        users = load_users()
        user = get_user_by_email(users, email)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        data = request.get_json(force=True) or {}
        if 'name' in data:
            user['name'] = data['name']
        if 'phone' in data:
            user['phone'] = data['phone']
        if 'profile' in data and isinstance(data['profile'], dict):
            user['profile'] = {**user.get('profile', {}), **data['profile']}

        users[email] = user
        save_users(users)

        public_user = {k: v for k, v in user.items() if k != 'password_hash'}
        return jsonify({'success': True, 'user': public_user})
    except jwt.ExpiredSignatureError:
        return jsonify({'success': False, 'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'success': False, 'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Auth: logout (stateless JWT)
@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    return jsonify({'success': True, 'message': 'Logged out'})

@app.route('/api/investment/analyze', methods=['POST'])
def analyze_investments():
    """Analyze different investment options"""
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'fixed_deposits')
        
        if analysis_type == 'fixed_deposits':
            results = investment_guide.analyze_fixed_deposits()
            return jsonify({
                'success': True,
                'type': 'fixed_deposits',
                'data': results.to_dict('records') if not results.empty else []
            })
        
        elif analysis_type == 'equity':
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            results = investment_guide.analyze_equity(start_date, end_date)
            return jsonify({
                'success': True,
                'type': 'equity',
                'data': results.to_dict('records') if not results.empty else []
            })
        
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid analysis type. Use "fixed_deposits" or "equity"'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/investment/recommendations', methods=['POST'])
def get_investment_recommendations():
    """Get personalized investment recommendations"""
    try:
        data = request.get_json()
        user_profile = {
            'risk_tolerance': data.get('risk_tolerance', 'moderate'),
            'age': data.get('age', 30),
            'income': data.get('income', 1000000),
            'investment_experience': data.get('experience', 'intermediate')
        }
        
        recommendations = investment_guide.get_investment_recommendations(user_profile)
        
        return jsonify({
            'success': True,
            'user_profile': user_profile,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/budget/optimize', methods=['POST'])
def optimize_budget():
    """Optimize budget based on user inputs"""
    try:
        data = request.get_json()
        
        # Create budget optimizer instance
        optimizer = BudgetOptimizer(
            monthly_income=data.get('monthly_income', 0),
            irregular_income=data.get('irregular_income', 0),
            irregular_freq=data.get('irregular_freq', 'monthly'),
            outstanding_loans=data.get('outstanding_loans', 0),
            emi=data.get('emi', 0),
            food_input=data.get('food_expenses', 0),
            leisure_input=data.get('leisure_expenses', 0),
            travel_input=data.get('travel_expenses', 0),
            fixed_costs=data.get('fixed_costs', 0),
            savings_input=data.get('current_savings', 0),
            monthly_savings_goal=data.get('savings_goal', 0),
            goal=data.get('goal', 'Save More'),
            extra_emi=data.get('extra_emi', 0),
            interest_rate=data.get('interest_rate', 0),
            loan_tenure=data.get('loan_tenure', 0),
            financial_goal_amount=data.get('financial_goal_amount', 0),
            months_to_goal=data.get('months_to_goal', 0)
        )
        
        # Optimize budget
        optimized_budget = optimizer.optimize_budget()
        
        # Get comprehensive analysis
        analysis = optimizer.get_budget_analysis()
        
        # Get financial goal progress if applicable
        goal_progress = optimizer.calculate_financial_goal_progress()
        
        return jsonify({
            'success': True,
            'optimized_budget': optimized_budget,
            'analysis': analysis,
            'goal_progress': goal_progress
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/portfolio/optimize', methods=['POST'])
def optimize_portfolio():
    """Optimize investment portfolio"""
    try:
        data = request.get_json()
        
        # Prepare user inputs for portfolio optimization
        user_inputs = {
            "age": data.get('age', 30),
            "annual_income": data.get('annual_income', 1000000),
            "total_savings": data.get('total_savings', 750000),
            "monthly_expenses": data.get('monthly_expenses', 30000),
            "investment_amount": data.get('investment_amount', 500000),
            "investment_horizon": data.get('investment_horizon', 10),
            "risk_tolerance": data.get('risk_tolerance', 'moderate'),
            "financial_goal": data.get('financial_goal', 1000000),
            "investment_experience": data.get('investment_experience', 'intermediate'),
            "liquidity_needs": data.get('liquidity_needs', 'moderate'),
            "tax_bracket": data.get('tax_bracket', 0.125),
            "expected_inflation": data.get('expected_inflation', 0.06)
        }
        
        # Optimize portfolio
        results = portfolio_optimizer.optimize_portfolio(user_inputs)
        
        if 'error' in results:
            return jsonify({
                'success': False,
                'error': results['error']
            }), 400
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chatbot/query', methods=['POST'])
def chatbot_query():
    """Handle AI chatbot queries"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Enhanced response system with more financial knowledge
        responses = {
            'save money': 'To save more money effectively: 1) Follow the 50/30/20 rule (50% needs, 30% wants, 20% savings), 2) Automate your savings transfers, 3) Track every expense for 30 days, 4) Use our Budget Optimizer tool for personalized recommendations, 5) Set up multiple savings goals (emergency fund, vacation, etc.).',
            'investment': 'Smart investment strategy: 1) Start with emergency fund (3-6 months expenses), 2) Consider your risk tolerance and time horizon, 3) Diversify across asset classes (equity, debt, gold), 4) Use SIPs for rupee cost averaging, 5) Review and rebalance annually. Use our Investment Guide for personalized recommendations.',
            'budget': 'Effective budgeting steps: 1) Track all income and expenses for 1 month, 2) Categorize expenses (needs vs wants), 3) Set realistic spending limits, 4) Use the 50/30/20 rule as a starting point, 5) Review and adjust monthly. Our Budget Optimizer provides AI-powered analysis and suggestions.',
            'emergency fund': 'Emergency fund guidelines: 1) Target 3-6 months of essential expenses, 2) Keep in high-yield savings account or liquid mutual funds, 3) Start with ₹10,000-50,000 and build gradually, 4) Only use for true emergencies (job loss, medical crisis), 5) Replenish immediately after use.',
            'mutual fund': 'Mutual fund investing: 1) Choose based on goals and risk tolerance, 2) Index funds offer lower fees and market returns, 3) Start with large-cap funds for stability, 4) Use SIPs for disciplined investing, 5) Avoid frequent switching. Consider our Investment Guide for fund selection.',
            'tax': 'Tax-saving strategies: 1) ELSS funds (₹1.5L under 80C), 2) PPF (₹1.5L, 15-year lock-in), 3) NPS (₹50K under 80CCD), 4) Health insurance (₹25K under 80D), 5) Home loan interest (₹2L under 24B). Consult a CA for complex situations.',
            'insurance': 'Insurance planning: 1) Life insurance: 10-15x annual income, 2) Health insurance: ₹5-10L coverage minimum, 3) Term insurance is most cost-effective, 4) Consider family floater plans, 5) Review coverage annually. Use our tools to calculate your insurance needs.',
            'retirement': 'Retirement planning essentials: 1) Start early (even ₹5,000/month at 25), 2) Use NPS for tax benefits, 3) Invest in equity for long-term growth, 4) Consider EPF and PPF, 5) Plan for 25-30 years post-retirement. Our Investment Guide calculates your retirement corpus needs.',
            'debt': 'Debt management strategy: 1) List all debts with interest rates, 2) Pay highest interest first (avalanche method), 3) Consider debt consolidation if rates are high, 4) Avoid new debt while paying existing, 5) Use windfalls (bonuses) to pay down debt. Our Budget Optimizer helps prioritize payments.',
            'credit score': 'Credit score improvement: 1) Pay all bills on time (35% of score), 2) Keep credit utilization below 30% (30% of score), 3) Maintain old credit accounts, 4) Limit new credit applications, 5) Check credit report annually. Aim for 750+ score.',
            'sip': 'SIP benefits: 1) Rupee cost averaging reduces market timing risk, 2) Disciplined investing habit, 3) Start with as low as ₹500/month, 4) Choose based on goals (short/medium/long-term), 5) Increase SIP amount annually. Use our Investment Guide for SIP planning.',
            'fd': 'Fixed deposits: 1) Safe but low returns (6-7%), 2) Good for emergency fund and short-term goals, 3) Compare rates across banks, 4) Consider tax implications, 5) Ladder FDs for liquidity. Better returns available in debt mutual funds.',
            'gold': 'Gold investment: 1) 5-10% of portfolio allocation, 2) Gold ETFs are more liquid than physical gold, 3) Sovereign Gold Bonds offer tax benefits, 4) Hedge against inflation, 5) Don\'t over-allocate. Use our Investment Guide for proper allocation.',
            'home loan': 'Home loan tips: 1) Compare rates across lenders, 2) Maintain good credit score for better rates, 3) Consider prepayment to save interest, 4) Factor in all costs (processing, insurance), 5) Use EMI calculator for affordability. Our Budget Optimizer helps plan for home purchase.',
            'child education': 'Education planning: 1) Start early (even before child is born), 2) Use SIPs in equity funds for long-term growth, 3) Consider education loans as backup, 4) Factor in inflation (education costs rise 10-12% annually), 5) Review and adjust annually. Our Investment Guide calculates education corpus needs.'
        }
        
        # Find matching response
        response = "I'd be happy to help with your financial question. Could you please provide more specific details about what you'd like to know? You can also try asking about saving money, investments, budgeting, or insurance."
        
        for key, value in responses.items():
            if key in user_message:
                response = value
                break
        
        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your AI financial assistant. I can help you with questions about personal finance, investments, budgeting, and financial planning. What would you like to know?"
        
        # Enhanced suggestions based on user query
        suggestions = [
                'How to save money?',
                'Investment advice',
                'Budget planning',
                'Emergency fund',
            'Tax saving tips',
            'SIP planning',
            'Home loan tips',
            'Child education planning',
            'Retirement planning',
            'Insurance planning'
        ]
        
        # Contextual suggestions based on query
        if any(word in user_message for word in ['save', 'budget', 'expense']):
            suggestions = ['Budget planning', 'Emergency fund', 'How to save money?', 'Debt management', 'Expense tracking']
        elif any(word in user_message for word in ['invest', 'mutual', 'sip', 'fund']):
            suggestions = ['Investment advice', 'SIP planning', 'Mutual fund selection', 'Portfolio diversification', 'Risk assessment']
        elif any(word in user_message for word in ['tax', '80c', 'ppf', 'nps']):
            suggestions = ['Tax saving tips', 'ELSS funds', 'PPF investment', 'NPS planning', 'Tax planning']
        elif any(word in user_message for word in ['insurance', 'life', 'health', 'term']):
            suggestions = ['Insurance planning', 'Life insurance', 'Health insurance', 'Term insurance', 'Family protection']
        elif any(word in user_message for word in ['retirement', 'pension', 'old age']):
            suggestions = ['Retirement planning', 'NPS investment', 'EPF planning', 'Pension planning', 'Senior citizen benefits']
        
        return jsonify({
            'success': True,
            'response': response,
            'suggestions': suggestions[:5]  # Limit to 5 suggestions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Enhanced Financial Calculations API
@app.route('/api/calculations/compound-interest', methods=['POST'])
def calculate_compound_interest():
    """Calculate compound interest for investments"""
    try:
        data = request.get_json()
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0)) / 100  # Convert percentage to decimal
        time = int(data.get('time', 0))
        frequency = data.get('frequency', 'annually')  # annually, monthly, quarterly
        
        # Convert frequency to number of times per year
        freq_map = {
            'annually': 1,
            'quarterly': 4,
            'monthly': 12,
            'daily': 365
        }
        n = freq_map.get(frequency, 1)
        
        # Compound interest formula: A = P(1 + r/n)^(nt)
        amount = principal * (1 + rate/n) ** (n * time)
        interest = amount - principal
        
        # Calculate year-by-year breakdown
        yearly_breakdown = []
        current_amount = principal
        for year in range(1, time + 1):
            current_amount = principal * (1 + rate/n) ** (n * year)
            yearly_interest = current_amount - principal
            yearly_breakdown.append({
                'year': year,
                'principal': principal,
                'interest_earned': round(yearly_interest, 2),
                'total_amount': round(current_amount, 2)
            })
        
        return jsonify({
            'success': True,
            'result': {
                'principal': principal,
                'rate': rate * 100,
                'time': time,
                'frequency': frequency,
                'final_amount': round(amount, 2),
                'total_interest': round(interest, 2),
                'yearly_breakdown': yearly_breakdown
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/calculations/sip-returns', methods=['POST'])
def calculate_sip_returns():
    """Calculate SIP returns with different scenarios"""
    try:
        data = request.get_json()
        monthly_investment = float(data.get('monthly_investment', 0))
        expected_return = float(data.get('expected_return', 0)) / 100
        time_period = int(data.get('time_period', 0))
        
        # Calculate SIP returns
        # Future Value = P * [((1 + r)^n - 1) / r] * (1 + r)
        # where P = monthly investment, r = monthly rate, n = number of months
        monthly_rate = expected_return / 12
        total_months = time_period * 12
        total_invested = monthly_investment * total_months
        
        if monthly_rate > 0:
            future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate) * (1 + monthly_rate)
        else:
            future_value = total_invested
        
        total_gains = future_value - total_invested
        
        # Calculate different return scenarios
        scenarios = []
        for return_rate in [6, 8, 10, 12, 15]:
            if return_rate != expected_return * 100:
                monthly_rate_scenario = return_rate / 100 / 12
                if monthly_rate_scenario > 0:
                    fv_scenario = monthly_investment * (((1 + monthly_rate_scenario) ** total_months - 1) / monthly_rate_scenario) * (1 + monthly_rate_scenario)
                else:
                    fv_scenario = total_invested
                scenarios.append({
                    'return_rate': return_rate,
                    'future_value': round(fv_scenario, 2),
                    'total_gains': round(fv_scenario - total_invested, 2)
                })
        
        return jsonify({
            'success': True,
            'result': {
                'monthly_investment': monthly_investment,
                'expected_return': expected_return * 100,
                'time_period': time_period,
                'total_invested': total_invested,
                'future_value': round(future_value, 2),
                'total_gains': round(total_gains, 2),
                'scenarios': scenarios
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/calculations/retirement-planning', methods=['POST'])
def calculate_retirement_planning():
    """Calculate retirement corpus needed and monthly SIP required"""
    try:
        data = request.get_json()
        current_age = int(data.get('current_age', 30))
        retirement_age = int(data.get('retirement_age', 60))
        current_income = float(data.get('current_income', 0))
        inflation_rate = float(data.get('inflation_rate', 6)) / 100
        expected_return = float(data.get('expected_return', 10)) / 100
        replacement_ratio = float(data.get('replacement_ratio', 80)) / 100  # 80% of current income
        
        years_to_retirement = retirement_age - current_age
        
        # Calculate retirement income needed (considering inflation)
        retirement_income = current_income * (1 + inflation_rate) ** years_to_retirement * replacement_ratio
        
        # Calculate retirement corpus needed (assuming 30 years post-retirement)
        post_retirement_years = 30
        monthly_retirement_income = retirement_income / 12
        
        # Calculate corpus using present value of annuity formula
        monthly_inflation = inflation_rate / 12
        monthly_return = expected_return / 12
        total_months = post_retirement_years * 12
        
        if monthly_return > monthly_inflation:
            real_rate = (1 + monthly_return) / (1 + monthly_inflation) - 1
            corpus = monthly_retirement_income * ((1 - (1 + real_rate) ** -total_months) / real_rate)
        else:
            corpus = monthly_retirement_income * total_months
        
        # Calculate monthly SIP needed to achieve this corpus
        total_months_sip = years_to_retirement * 12
        monthly_sip_rate = expected_return / 12
        
        if monthly_sip_rate > 0:
            required_sip = corpus / (((1 + monthly_sip_rate) ** total_months_sip - 1) / monthly_sip_rate) / (1 + monthly_sip_rate)
        else:
            required_sip = corpus / total_months_sip
        
        return jsonify({
            'success': True,
            'result': {
                'current_age': current_age,
                'retirement_age': retirement_age,
                'years_to_retirement': years_to_retirement,
                'current_income': current_income,
                'retirement_income_needed': round(retirement_income, 2),
                'retirement_corpus_needed': round(corpus, 2),
                'monthly_sip_required': round(required_sip, 2),
                'total_sip_investment': round(required_sip * total_months_sip, 2),
                'expected_corpus': round(required_sip * (((1 + monthly_sip_rate) ** total_months_sip - 1) / monthly_sip_rate) * (1 + monthly_sip_rate), 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/calculations/loan-emi', methods=['POST'])
def calculate_loan_emi():
    """Calculate EMI for different types of loans"""
    try:
        data = request.get_json()
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0)) / 100
        tenure = int(data.get('tenure', 0))
        loan_type = data.get('loan_type', 'home')  # home, personal, car, education
        
        # Convert annual rate to monthly rate
        monthly_rate = rate / 12
        total_months = tenure * 12
        
        # EMI calculation: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        if monthly_rate > 0:
            emi = principal * monthly_rate * (1 + monthly_rate) ** total_months / ((1 + monthly_rate) ** total_months - 1)
        else:
            emi = principal / total_months
        
        total_payment = emi * total_months
        total_interest = total_payment - principal
        
        # Calculate year-wise breakdown
        yearly_breakdown = []
        remaining_principal = principal
        
        for year in range(1, tenure + 1):
            year_principal = 0
            year_interest = 0
            
            for month in range(12):
                if remaining_principal > 0:
                    interest_payment = remaining_principal * monthly_rate
                    principal_payment = emi - interest_payment
                    
                    if principal_payment > remaining_principal:
                        principal_payment = remaining_principal
                    
                    year_principal += principal_payment
                    year_interest += interest_payment
                    remaining_principal -= principal_payment
            
            yearly_breakdown.append({
                'year': year,
                'principal_paid': round(year_principal, 2),
                'interest_paid': round(year_interest, 2),
                'remaining_principal': round(remaining_principal, 2)
            })
        
        return jsonify({
            'success': True,
            'result': {
                'principal': principal,
                'rate': rate * 100,
                'tenure': tenure,
                'loan_type': loan_type,
                'monthly_emi': round(emi, 2),
                'total_payment': round(total_payment, 2),
                'total_interest': round(total_interest, 2),
                'yearly_breakdown': yearly_breakdown
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/market-data/indices', methods=['GET'])
def get_market_indices():
    """Get current market indices (simulated data)"""
    try:
        # In a real application, you would fetch this from a financial API
        # For now, we'll simulate with realistic data
        indices = {
            'nifty_50': {
                'name': 'Nifty 50',
                'value': 21500 + random.randint(-500, 500),
                'change': round(random.uniform(-2, 2), 2),
                'change_percent': round(random.uniform(-1, 1), 2)
            },
            'sensex': {
                'name': 'BSE Sensex',
                'value': 71000 + random.randint(-1500, 1500),
                'change': round(random.uniform(-2, 2), 2),
                'change_percent': round(random.uniform(-1, 1), 2)
            },
            'nifty_bank': {
                'name': 'Nifty Bank',
                'value': 48000 + random.randint(-1000, 1000),
                'change': round(random.uniform(-2, 2), 2),
                'change_percent': round(random.uniform(-1, 1), 2)
            },
            'nifty_it': {
                'name': 'Nifty IT',
                'value': 35000 + random.randint(-800, 800),
                'change': round(random.uniform(-2, 2), 2),
                'change_percent': round(random.uniform(-1, 1), 2)
            }
        }
        
        return jsonify({
            'success': True,
            'data': indices,
            'last_updated': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/market-data/mutual-funds', methods=['GET'])
def get_mutual_fund_data():
    """Get mutual fund performance data (simulated)"""
    try:
        # Simulate mutual fund data
        fund_categories = ['Large Cap', 'Mid Cap', 'Small Cap', 'Balanced', 'Debt', 'ELSS']
        funds = []
        
        for category in fund_categories:
            for i in range(3):  # 3 funds per category
                fund_name = f"{category} Fund {i+1}"
                current_nav = round(random.uniform(50, 500), 2)
                one_year_return = round(random.uniform(-5, 25), 2)
                three_year_return = round(random.uniform(5, 35), 2)
                five_year_return = round(random.uniform(8, 40), 2)
                
                funds.append({
                    'name': fund_name,
                    'category': category,
                    'current_nav': current_nav,
                    'one_year_return': one_year_return,
                    'three_year_return': three_year_return,
                    'five_year_return': five_year_return,
                    'risk_level': random.choice(['Low', 'Medium', 'High']),
                    'expense_ratio': round(random.uniform(0.5, 2.5), 2)
                })
        
        return jsonify({
            'success': True,
            'data': funds,
            'last_updated': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/calculations/tax-calculator', methods=['POST'])
def calculate_tax():
    """Calculate income tax for different income levels"""
    try:
        data = request.get_json()
        annual_income = float(data.get('annual_income', 0))
        age = int(data.get('age', 30))
        deductions = float(data.get('deductions', 0))  # 80C, 80D, etc.
        
        # Tax slabs for FY 2024-25 (New Tax Regime)
        taxable_income = annual_income - deductions
        
        if age < 60:
            # Regular tax slabs
            if taxable_income <= 300000:
                tax = 0
            elif taxable_income <= 600000:
                tax = (taxable_income - 300000) * 0.05
            elif taxable_income <= 900000:
                tax = 15000 + (taxable_income - 600000) * 0.10
            elif taxable_income <= 1200000:
                tax = 45000 + (taxable_income - 900000) * 0.15
            elif taxable_income <= 1500000:
                tax = 90000 + (taxable_income - 1200000) * 0.20
            else:
                tax = 150000 + (taxable_income - 1500000) * 0.30
        else:
            # Senior citizen tax slabs (simplified)
            if taxable_income <= 300000:
                tax = 0
            elif taxable_income <= 500000:
                tax = (taxable_income - 300000) * 0.05
            elif taxable_income <= 1000000:
                tax = 10000 + (taxable_income - 500000) * 0.20
            else:
                tax = 110000 + (taxable_income - 1000000) * 0.30
        
        # Add cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        # Calculate effective tax rate
        effective_rate = (total_tax / annual_income) * 100 if annual_income > 0 else 0
        
        return jsonify({
            'success': True,
            'result': {
                'annual_income': annual_income,
                'deductions': deductions,
                'taxable_income': taxable_income,
                'tax_before_cess': round(tax, 2),
                'cess': round(cess, 2),
                'total_tax': round(total_tax, 2),
                'effective_tax_rate': round(effective_rate, 2),
                'take_home_income': round(annual_income - total_tax, 2)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# Email Notification System
def send_email(to_email, subject, body, is_html=False):
    """Send email notification"""
    try:
        # Email configuration (use environment variables in production)
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_username = os.environ.get('SMTP_USERNAME', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        if not smtp_username or not smtp_password:
            return False, "Email configuration not set"
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_username, to_email, text)
        server.quit()
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)

@app.route('/api/notifications/send', methods=['POST'])
@jwt_required
def send_notification(current_user):
    """Send notification to user"""
    try:
        data = request.get_json()
        notification_type = data.get('type', 'general')
        message = data.get('message', '')
        user_email = current_user.get('email')
        
        if not user_email:
            return jsonify({'success': False, 'error': 'User email not found'}), 400
        
        # Create email content based on notification type
        if notification_type == 'welcome':
            subject = "Welcome to Ghar Ka Guide!"
            body = f"""
            <html>
            <body>
                <h2>Welcome to Ghar Ka Guide!</h2>
                <p>Dear {current_user.get('name', 'User')},</p>
                <p>Thank you for joining Ghar Ka Guide. We're excited to help you achieve your financial goals!</p>
                <p>Here are some things you can do to get started:</p>
                <ul>
                    <li>Complete your profile setup</li>
                    <li>Try our Budget Optimizer tool</li>
                    <li>Explore our Investment Guide</li>
                    <li>Chat with our AI assistant for personalized advice</li>
                </ul>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p>Best regards,<br>Ghar Ka Guide Team</p>
            </body>
            </html>
            """
        elif notification_type == 'budget_reminder':
            subject = "Monthly Budget Review Reminder"
            body = f"""
            <html>
            <body>
                <h2>Time for Your Monthly Budget Review</h2>
                <p>Dear {current_user.get('name', 'User')},</p>
                <p>It's time to review your monthly budget and track your progress towards your financial goals.</p>
                <p>Log in to your dashboard to:</p>
                <ul>
                    <li>Update your income and expenses</li>
                    <li>Review your spending patterns</li>
                    <li>Adjust your budget for next month</li>
                    <li>Check your savings progress</li>
                </ul>
                <p>Stay on track with your financial goals!</p>
                <p>Best regards,<br>Ghar Ka Guide Team</p>
            </body>
            </html>
            """
        elif notification_type == 'investment_update':
            subject = "Investment Portfolio Update"
            body = f"""
            <html>
            <body>
                <h2>Your Investment Portfolio Update</h2>
                <p>Dear {current_user.get('name', 'User')},</p>
                <p>Here's your monthly investment portfolio update:</p>
                <p>Market conditions and your portfolio performance have been analyzed. Consider reviewing your investment strategy.</p>
                <p>Log in to see detailed insights and recommendations.</p>
                <p>Best regards,<br>Ghar Ka Guide Team</p>
            </body>
            </html>
            """
        else:
            subject = "Notification from Ghar Ka Guide"
            body = message
        
        # Send email
        success, error_msg = send_email(user_email, subject, body, is_html=True)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Notification sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to send notification: {error_msg}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name', 'Subscriber')
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Send welcome email
        subject = "Welcome to Ghar Ka Guide Newsletter!"
        body = f"""
        <html>
        <body>
            <h2>Thank you for subscribing!</h2>
            <p>Dear {name},</p>
            <p>Welcome to the Ghar Ka Guide newsletter! You'll now receive:</p>
            <ul>
                <li>Weekly financial tips and insights</li>
                <li>Market updates and analysis</li>
                <li>New feature announcements</li>
                <li>Exclusive content and guides</li>
            </ul>
            <p>We're committed to helping you make informed financial decisions.</p>
            <p>Best regards,<br>Ghar Ka Guide Team</p>
        </body>
        </html>
        """
        
        success, error_msg = send_email(email, subject, body, is_html=True)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Successfully subscribed to newsletter'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to subscribe: {error_msg}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/test', methods=['POST'])
def test_notification():
    """Test notification system"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        subject = "Test Notification from Ghar Ka Guide"
        body = """
        <html>
        <body>
            <h2>Test Notification</h2>
            <p>This is a test notification to verify that our email system is working correctly.</p>
            <p>If you received this email, the notification system is functioning properly.</p>
            <p>Best regards,<br>Ghar Ka Guide Team</p>
        </body>
        </html>
        """
        
        success, error_msg = send_email(email, subject, body, is_html=True)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Test notification sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to send test notification: {error_msg}'
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Ollama-powered chatbot (Chatbot_Final_Ollama.ipynb integration)
@app.route('/api/chatbot/ollama', methods=['POST'])
def chatbot_ollama():
    """Proxy chatbot requests to a local Ollama server using a finance-focused system prompt."""
    try:
        data = request.get_json(force=True) or {}
        user_message = (data.get('message') or '').strip()
        history = data.get('history') or []  # optional: [{role:'user'|'assistant', content:'...'}]

        if not user_message and not history:
            return jsonify({'success': False, 'error': 'message is required'}), 400

        ollama_base_url = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
        ollama_model = os.environ.get('OLLAMA_MODEL', 'llama3.1')
        chat_url = f"{ollama_base_url}/api/chat"

        # Compose messages for Ollama
        messages = [{
            'role': 'system',
            'content': (
                "You are an Indian personal finance assistant for Ghar Ka Guide. "
                "Answer clearly and practically for users in India (₹, SIPs, ELSS, EPF/PPF, NPS, tax slabs, etc.). "
                "Keep answers concise, with bullet points where helpful. Avoid giving legal or investment guarantees."
            )
        }]

        # Append prior turns if provided
        for turn in history:
            if isinstance(turn, dict) and 'role' in turn and 'content' in turn:
                role = 'assistant' if turn.get('role') == 'assistant' else 'user'
                messages.append({'role': role, 'content': str(turn.get('content') or '')})

        if user_message:
            messages.append({'role': 'user', 'content': user_message})

        payload = {
            'model': ollama_model,
            'messages': messages,
            'stream': False
        }

        resp = requests.post(chat_url, json=payload, timeout=60)
        resp.raise_for_status()
        llm = resp.json()

        reply = ''
        if isinstance(llm, dict):
            # Ollama chat returns {'message': {'role': 'assistant', 'content': '...'}}
            if isinstance(llm.get('message'), dict):
                reply = llm['message'].get('content') or ''
            # Fallbacks (in case of different formats)
            elif isinstance(llm.get('choices'), list) and llm['choices']:
                reply = (llm['choices'][0].get('message') or {}).get('content', '')

        return jsonify({'success': True, 'response': reply})
    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'error': f'Ollama request failed: {e}'}), 502
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Error logging endpoint
ERRORS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'errors.json')

@app.route('/api/errors/log', methods=['POST'])
def log_error():
    """Log client-side errors for debugging"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        error_entry = {
            'timestamp': data.get('timestamp', datetime.datetime.now().isoformat()),
            'message': data.get('message', 'Unknown error'),
            'stack': data.get('stack', ''),
            'url': data.get('url', ''),
            'userAgent': data.get('userAgent', ''),
            'context': data.get('context', {})
        }

        # Load existing errors
        errors = []
        if os.path.exists(ERRORS_FILE):
            try:
                with open(ERRORS_FILE, 'r', encoding='utf-8') as f:
                    errors = json.load(f)
            except:
                errors = []

        # Add new error (keep last 1000 errors)
        errors.append(error_entry)
        if len(errors) > 1000:
            errors = errors[-1000:]

        # Save errors
        with open(ERRORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)

        # In production, you might want to send to Sentry, LogRocket, etc.
        print(f"⚠️ Error logged: {error_entry['message']}")

        return jsonify({'success': True})
    except Exception as e:
        print(f"Failed to log error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytics tracking endpoint
ANALYTICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analytics.json')

@app.route('/api/analytics/track', methods=['POST'])
def track_analytics():
    """Track custom analytics events"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        event_entry = {
            'timestamp': data.get('timestamp', datetime.datetime.now().isoformat()),
            'event': data.get('event', 'unknown'),
            'properties': data.get('properties', {}),
            'url': data.get('url', '')
        }

        # Load existing analytics
        analytics = []
        if os.path.exists(ANALYTICS_FILE):
            try:
                with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                    analytics = json.load(f)
            except:
                analytics = []

        # Add new event (keep last 5000 events)
        analytics.append(event_entry)
        if len(analytics) > 5000:
            analytics = analytics[-5000:]

        # Save analytics
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True})
    except Exception as e:
        print(f"Failed to track analytics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/stats', methods=['GET'])
def get_analytics_stats():
    """Get analytics statistics (for admin dashboard)"""
    try:
        if not os.path.exists(ANALYTICS_FILE):
            return jsonify({'success': True, 'stats': {}})

        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
            analytics = json.load(f)

        # Calculate basic stats
        events = {}
        page_views = {}
        for entry in analytics:
            event_name = entry.get('event', 'unknown')
            events[event_name] = events.get(event_name, 0) + 1
            
            if event_name == 'page_view':
                path = entry.get('properties', {}).get('path', 'unknown')
                page_views[path] = page_views.get(path, 0) + 1

        return jsonify({
            'success': True,
            'stats': {
                'total_events': len(analytics),
                'event_counts': events,
                'page_views': page_views
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Development mode
    print("🚀 Starting Ghar Ka Guide Financial API Server...")
    print("📊 Available endpoints:")
    print("   - GET  / - API information")
    print("   - POST /api/investment/analyze - Investment analysis")
    print("   - POST /api/budget/optimize - Budget optimization")
    print("   - POST /api/portfolio/optimize - Portfolio optimization")
    print("   - POST /api/chatbot/query - AI chatbot")
    print("   - POST /api/errors/log - Error logging")
    print("   - POST /api/analytics/track - Analytics tracking")
    print("\n🌐 Server running on http://localhost:5000")
    print("💡 Use Ctrl+C to stop the server")
    
    # Only run in debug mode for local development
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

