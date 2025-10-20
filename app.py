from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
import os
import datetime
import bcrypt
import jwt

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our financial tools
from investment_guide import InvestmentGuide
from budget_optimizer import BudgetOptimizer
from portfolio_optimizer import PortfolioOptimizer

app = Flask(__name__)
CORS(app)

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

# Initialize our tools
investment_guide = InvestmentGuide()
portfolio_optimizer = PortfolioOptimizer()

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
        
        # Simple response system (you can enhance this with your AI model)
        responses = {
            'save money': 'To save more money, try the 50/30/20 rule: 50% for needs, 30% for wants, 20% for savings. Also, automate your savings and track all expenses.',
            'investment': 'Good investment options include mutual funds, fixed deposits, government bonds, and gold ETFs. Your choice depends on risk tolerance and time horizon.',
            'budget': 'Create a budget by tracking income, categorizing expenses, setting spending limits, and reviewing monthly. Use our Budget Optimizer tool for detailed analysis.',
            'emergency fund': 'Aim for 3-6 months of expenses in your emergency fund. Start small and build gradually. Keep it in a separate, easily accessible account.',
            'mutual fund': 'Mutual funds are a great way to invest in the stock market with professional management. Consider index funds for lower fees and better returns.',
            'tax': 'Tax-saving investments include ELSS, PPF, and NPS. Consult a tax advisor for personalized advice based on your income bracket.',
            'insurance': 'Life insurance should cover 10-15 times your annual income. Health insurance is essential for medical emergencies.',
            'retirement': 'Start retirement planning early. Use our Investment Guide tool to create a personalized retirement strategy.',
            'debt': 'Focus on paying high-interest debt first (credit cards, personal loans). Consider debt consolidation for better rates.',
            'credit score': 'Maintain a good credit score by paying bills on time, keeping credit utilization low, and avoiding too many credit inquiries.'
        }
        
        # Find matching response
        response = "I'd be happy to help with your financial question. Could you please provide more specific details about what you'd like to know? You can also try asking about saving money, investments, budgeting, or insurance."
        
        for key, value in responses.items():
            if key in user_message:
                response = value
                break
        
        if any(word in user_message for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your AI financial assistant. I can help you with questions about personal finance, investments, budgeting, and financial planning. What would you like to know?"
        
        return jsonify({
            'success': True,
            'response': response,
            'suggestions': [
                'How to save money?',
                'Investment advice',
                'Budget planning',
                'Emergency fund',
                'Tax saving tips'
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Ghar Ka Guide Financial API Server...")
    print("📊 Available endpoints:")
    print("   - GET  / - API information")
    print("   - POST /api/investment/analyze - Investment analysis")
    print("   - POST /api/budget/optimize - Budget optimization")
    print("   - POST /api/portfolio/optimize - Portfolio optimization")
    print("   - POST /api/chatbot/query - AI chatbot")
    print("\n🌐 Server running on http://localhost:5000")
    print("💡 Use Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

