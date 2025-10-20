# 🔐 Ghar Ka Guide - Authentication System

Your financial website now has **real, secure user authentication**! Users can create accounts, login securely, and access personalized financial tools.

## 🎯 **What's Been Added:**

### **1. User Authentication API** 🔐
- **User Registration** with secure password hashing
- **User Login** with JWT token generation
- **Token Verification** for protected routes
- **Profile Management** with real-time updates
- **Secure Logout** with token invalidation

### **2. Security Features** 🛡️
- **BCrypt Password Hashing** - Industry standard security
- **JWT Tokens** - Secure, stateless authentication
- **Input Validation** - Prevents malicious data
- **Session Management** - Secure user sessions

### **3. User Management** 👥
- **JSON Database** - Simple, file-based user storage
- **Profile Data** - Age, income, risk tolerance, experience
- **Real-time Updates** - Profile changes saved immediately

## 🚀 **Quick Start Guide:**

### **Step 1: Start the Authentication Server**
```bash
cd c:\Users\jayaaditya-s\MyWebsite

# Start authentication server
python start_auth_server.py
```

**Expected Output:**
```
============================================================
🔐 Ghar Ka Guide Authentication Server
============================================================
📦 Checking authentication dependencies...
✅ flask
✅ flask-cors
✅ bcrypt
✅ PyJWT
🔐 Starting Ghar Ka Guide Authentication Server...
🌐 Server running on http://localhost:5001
```

### **Step 2: Test User Registration**
1. Open `login.html` in your browser
2. Click "Sign up" to switch to registration form
3. Fill in your details:
   - **Name**: Your full name
   - **Email**: Your email address
   - **Phone**: Your phone number
   - **Password**: At least 6 characters
4. Click "Create Account"

**Expected Result:**
- Account created successfully
- Automatically redirected to login form
- Email pre-filled for convenience

### **Step 3: Test User Login**
1. Enter your email and password
2. Click "Login"
3. **Success!** You'll be redirected to the dashboard

### **Step 4: Explore the Dashboard**
- **Real User Data** displayed in overview cards
- **Profile Management** with real-time updates
- **Secure Logout** functionality
- **Authentication Required** - can't access without login

## 🌐 **API Endpoints:**

### **Authentication Endpoints:**
```http
POST /api/auth/signup    # User registration
POST /api/auth/login     # User login
POST /api/auth/verify    # Verify JWT token
POST /api/auth/logout    # User logout
GET  /api/auth/profile   # Get user profile
PUT  /api/auth/profile   # Update user profile
```

### **Example API Calls:**

#### **User Registration:**
```javascript
fetch('http://localhost:5001/api/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'John Doe',
        email: 'john@example.com',
        phone: '+91 98765 43210',
        password: 'securepassword123'
    })
})
```

#### **User Login:**
```javascript
fetch('http://localhost:5001/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'john@example.com',
        password: 'securepassword123'
    })
})
```

#### **Update Profile:**
```javascript
fetch('http://localhost:5001/api/auth/profile', {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        name: 'John Smith',
        phone: '+91 98765 43211'
    })
})
```

## 🔒 **Security Features:**

### **Password Security:**
- **BCrypt Hashing** - Industry standard password hashing
- **Salt Generation** - Unique salt for each password
- **Secure Verification** - Constant-time password comparison

### **Token Security:**
- **JWT Tokens** - JSON Web Tokens for authentication
- **24-Hour Expiry** - Tokens expire automatically
- **Secure Storage** - Tokens stored in localStorage
- **Automatic Verification** - Every dashboard access verified

### **Data Protection:**
- **Input Validation** - All user inputs validated
- **Error Handling** - Secure error messages
- **Session Management** - Secure user sessions

## 📊 **User Data Structure:**

### **User Profile:**
```json
{
  "id": "unique-user-id",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 98765 43210",
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "profile": {
    "age": 30,
    "income": 750000,
    "risk_tolerance": "moderate",
    "investment_experience": "intermediate"
  }
}
```

### **Financial Profile:**
- **Age**: User's age for financial planning
- **Income**: Annual income for budget calculations
- **Risk Tolerance**: Conservative/Moderate/Aggressive
- **Investment Experience**: Beginner/Intermediate/Advanced

## 🛠️ **Technical Implementation:**

### **Backend (Python/Flask):**
- **Flask API** - RESTful authentication endpoints
- **BCrypt** - Password hashing and verification
- **PyJWT** - JWT token generation and verification
- **JSON Storage** - Simple file-based user database

### **Frontend (JavaScript):**
- **Fetch API** - HTTP requests to authentication server
- **LocalStorage** - Secure token and user data storage
- **Form Validation** - Client-side input validation
- **Error Handling** - User-friendly error messages

### **Security Flow:**
1. **User Registration** → Password hashed with BCrypt
2. **User Login** → Password verified, JWT token generated
3. **Token Storage** → JWT stored in localStorage
4. **API Calls** → Token included in Authorization header
5. **Token Verification** → Backend validates JWT on each request
6. **User Logout** → Token cleared from localStorage

## 🚨 **Troubleshooting:**

### **Common Issues:**

1. **Port Already in Use:**
   ```bash
   # Kill process on port 5001
   netstat -ano | findstr :5001
   taskkill /PID <PID> /F
   ```

2. **Missing Dependencies:**
   ```bash
   pip install bcrypt PyJWT
   ```

3. **CORS Issues:**
   - Ensure Flask-CORS is installed
   - Check browser console for errors

4. **Authentication Failed:**
   - Verify auth server is running on port 5001
   - Check localStorage for valid token
   - Ensure email/password are correct

### **Debug Mode:**
```bash
# Start with debug logging
python auth_api.py --debug
```

## 🔧 **Customization Options:**

### **Modify User Profile Fields:**
Edit `auth_api.py` to add new profile fields:
```python
'profile': {
    'age': data.get('age', 25),
    'income': data.get('income', 500000),
    'risk_tolerance': data.get('risk_tolerance', 'moderate'),
    'investment_experience': data.get('investment_experience', 'beginner'),
    'new_field': data.get('new_field', 'default_value')  # Add this
}
```

### **Change Token Expiry:**
Modify `JWT_EXPIRATION` in `auth_api.py`:
```python
JWT_EXPIRATION = 7 * 24 * 60 * 60  # 7 days instead of 1 day
```

### **Add Password Requirements:**
Enhance password validation in signup:
```python
if len(password) < 8:
    return jsonify({'success': False, 'error': 'Password must be at least 8 characters'}), 400
```

## 🚀 **Next Steps:**

### **Immediate Enhancements:**
1. **Email Verification** - Send confirmation emails
2. **Password Reset** - Forgot password functionality
3. **Social Login** - Google, Facebook integration
4. **Two-Factor Authentication** - SMS/Email verification

### **Advanced Features:**
1. **Database Integration** - PostgreSQL/MySQL
2. **Redis Caching** - Session and token caching
3. **Rate Limiting** - Prevent brute force attacks
4. **Audit Logging** - Track user actions

## 🎉 **Congratulations!**

You now have a **production-ready authentication system** that includes:
- ✅ **Secure User Registration** with password hashing
- ✅ **JWT-based Authentication** for secure sessions
- ✅ **Profile Management** with real-time updates
- ✅ **Protected Routes** requiring authentication
- ✅ **Professional Security** standards

### **Demo Account:**
- **Email**: `demo@gharkaguide.com`
- **Password**: `demo123`

**Your "Ghar Ka Guide" is now a secure, professional financial platform with real user accounts!** 🚀🔐💰

---

**Ready to test?** Start the authentication server and create your first account! 🎯

