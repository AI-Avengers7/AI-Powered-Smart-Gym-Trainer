# 🔧 Troubleshooting Guide

## "Method Not Allowed" Error

This error occurs when you try to access a URL with the wrong HTTP method.

### Common Causes:

1. **Accessing POST endpoints with GET**
   - ❌ Visiting `/auth/register` in browser → Error
   - ✅ Use API client (Postman) or form submission

2. **Wrong URL**
   - ❌ `/workout` → Method Not Allowed
   - ✅ `/workout/` (with trailing slash)

---

## 📋 All Available Routes

Visit http://localhost:5000/routes to see all available endpoints.

### **Pages (GET - Browser accessible)**
```
✅ http://localhost:5000/                    - Home page
✅ http://localhost:5000/auth/login          - Login page
✅ http://localhost:5000/auth/signup         - Signup page
✅ http://localhost:5000/workout/            - Workout page
✅ http://localhost:5000/analytics/          - Analytics dashboard
✅ http://localhost:5000/setup-camera        - Camera setup
✅ http://localhost:5000/suggestions         - Workout suggestions
✅ http://localhost:5000/analytics/history_page - Workout history page
```

### **API Endpoints (POST - Need API client or JavaScript)**

#### Authentication APIs:
```
POST /auth/register      - Register new user
POST /auth/login         - Login (also accepts GET)
GET  /auth/logout        - Logout
GET  /auth/profile       - Get current user profile
GET  /auth/user/<id>     - Get user by ID
PUT  /auth/user/<id>     - Update user
DELETE /auth/user/<id>   - Delete user
```

#### Workout APIs:
```
POST /workout/log              - Log workout
GET  /workout/history          - Get workout history (API)
GET  /workout/<id>             - Get specific workout
PUT  /workout/<id>             - Update workout
DELETE /workout/<id>           - Delete workout
GET  /workout/exercise/<name>  - Get workouts by exercise
GET  /workout/total-reps       - Get total reps
POST /workout/reset-count      - Reset rep counter
```

#### Analytics APIs:
```
GET /analytics/summary                  - Overall summary
GET /analytics/breakdown                - Exercise breakdown
GET /analytics/progress/<exercise>      - Progress for exercise
GET /analytics/recent                   - Recent activity
GET /analytics/records                  - Personal records
GET /analytics/exercise/<exercise>/stats - Exercise statistics
GET /analytics/history                  - Workout history (API)
```

---

## 🔍 How to Debug

### 1. Check Your URL
Make sure you're using the correct URL with proper spelling:
```bash
# List all routes
curl http://localhost:5000/routes
```

### 2. Check HTTP Method
Use the right method:
- **Browser** → Only GET requests
- **Forms** → POST requests
- **JavaScript/API** → Any method

### 3. Test with cURL
```bash
# Test GET request
curl http://localhost:5000/

# Test POST request
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"test123"}'
```

---

## 🐛 Common Errors & Fixes

### Error: "Method Not Allowed"
**Cause**: Wrong HTTP method or missing trailing slash

**Fix**:
```bash
# Wrong
curl http://localhost:5000/workout  # Missing slash

# Correct
curl http://localhost:5000/workout/
```

### Error: "404 Not Found"
**Cause**: URL doesn't exist

**Fix**: Check available routes at `/routes`

### Error: "No data provided"
**Cause**: POST request without JSON body

**Fix**:
```bash
# Add Content-Type and data
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@test.com","password":"pass123"}'
```

### Error: "Token has expired" or "Missing token"
**Cause**: JWT token expired or not provided

**Fix**: Login again to get new token

---

## 🧪 Testing the Application

### Test 1: Homepage (GET)
```bash
curl http://localhost:5000/
# Expected: HTML content of index.html
```

### Test 2: Login Page (GET)
```bash
curl http://localhost:5000/auth/login
# Expected: HTML content of login.html
```

### Test 3: Register User (POST)
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
# Expected: {"message": "User registered successfully"}
```

### Test 4: Login User (POST)
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
# Expected: {"access_token": "...", "user_id": 1}
```

### Test 5: Workout Page (GET)
```bash
curl http://localhost:5000/workout/
# Expected: HTML content of workout.html
```

---

## 🔄 Fixed Issues

### ✅ Login/Signup Routes
**Before**: Separate routes for GET and POST caused conflicts
**After**: Combined routes accept both methods

```python
# Old (caused errors)
@auth_bp.route('/login', methods=['GET'])
def login_page(): ...

@auth_bp.route('/login', methods=['POST'])
def login(): ...

# New (works correctly)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    # Handle POST...
```

---

## 📱 Browser vs API Testing

### Browser Testing (GET only)
```
✅ http://localhost:5000/
✅ http://localhost:5000/auth/login
✅ http://localhost:5000/workout/
✅ http://localhost:5000/analytics/
```

### API Testing (All methods)
Use Postman, Insomnia, or cURL:
```bash
# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@test.com","password":"test123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

---

## 🎯 Quick Fixes

### Restart the Server
```bash
# Stop current server (Ctrl+C)
# Then restart
./start.sh
```

### Clear Browser Cache
Press: `Ctrl + Shift + R` (hard refresh)

### Check Server Logs
Look at terminal output for error messages

### View All Routes
Navigate to: http://localhost:5000/routes

---

## ✅ Verification Checklist

- [ ] Server is running (`./start.sh`)
- [ ] No errors in terminal
- [ ] Homepage loads: http://localhost:5000/
- [ ] Login page loads: http://localhost:5000/auth/login
- [ ] Workout page loads: http://localhost:5000/workout/
- [ ] Routes page loads: http://localhost:5000/routes

---

## 🆘 Still Having Issues?

1. **Check terminal output** for specific error messages
2. **Visit /routes** to see all available endpoints
3. **Use cURL** to test API endpoints
4. **Check browser console** (F12) for JavaScript errors
5. **Verify database** exists: `ls -la test_gym_trainer.db`

---

## 📞 Need Help?

If you're still stuck, provide:
1. The exact URL you're trying to access
2. The HTTP method (GET, POST, etc.)
3. Any error messages in terminal or browser
4. Output from http://localhost:5000/routes
