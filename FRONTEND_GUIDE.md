# 🎨 Frontend Startup Guide

## 🚀 Quick Start

The frontend is integrated with the Flask backend. To start everything:

### **Method 1: Using the start script (Recommended)**
```bash
./start.sh
```

### **Method 2: Manual start**
```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run the application
python3 app.py
```

---

## 🌐 Available Pages

Once the server is running, you can access:

### **Main Pages:**
- **Home Page**: http://localhost:5000
- **Login**: http://localhost:5000/auth/login  
- **Sign Up**: http://localhost:5000/auth/signup
- **Workout**: http://localhost:5000/workout/
- **Analytics**: http://localhost:5000/analytics/
- **Camera Setup**: http://localhost:5000/setup-camera
- **Suggestions**: http://localhost:5000/suggestions
- **Workout History**: http://localhost:5000/analytics/history_page

---

## 📁 Frontend File Structure

```
app/views/
├── templates/           # HTML files
│   ├── index.html      # Landing page
│   ├── login.html      # Login page
│   ├── signup.html     # Registration page
│   ├── workout.html    # Main workout page
│   ├── analytics.html  # Analytics dashboard
│   ├── workout_history.html
│   ├── setup_camera.html
│   ├── suggestions.html
│   └── ...
├── static/
│   ├── css/
│   │   └── styles.css  # Custom styles
│   └── js/
│       ├── main.js     # Main JavaScript
│       └── workout.js  # Workout specific JS
```

---

## 🎨 Frontend Technologies

- **HTML5** - Structure
- **Tailwind CSS** - Styling (loaded via CDN)
- **Vanilla JavaScript** - Interactivity
- **Socket.IO** - Real-time WebSocket communication
- **Flask Templates** - Server-side rendering

---

## 🔧 How It Works

1. **Flask Backend** serves the HTML templates
2. **Templates** are in `app/views/templates/`
3. **Static files** (CSS, JS) are in `app/views/static/`
4. **WebSocket** connects frontend to backend for real-time pose detection

---

## 🚦 Starting the Application

### **Step 1: Ensure Virtual Environment is Active**
```bash
source venv/bin/activate
```
You should see `(venv)` in your terminal prompt.

### **Step 2: Start the Server**
```bash
python3 app.py
```

You should see:
```
Database tables created successfully!
* Running on http://0.0.0.0:5000
* Press CTRL+C to quit
```

### **Step 3: Open Your Browser**
Navigate to: **http://localhost:5000**

---

## 🎯 Testing the Frontend

### **1. Homepage Test**
```bash
curl http://localhost:5000
```
Should return HTML content.

### **2. API Test**
```bash
# Test user registration
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'
```

### **3. Browser Test**
Open http://localhost:5000 in your browser.

---

## 🌟 Key Features Available

### **Authentication**
- ✅ User registration
- ✅ User login
- ✅ Session management

### **Workout**
- ✅ Real-time pose detection
- ✅ Rep counting
- ✅ Exercise tracking
- ✅ WebSocket communication

### **Analytics**
- ✅ Workout history
- ✅ Progress charts
- ✅ Personal records
- ✅ Exercise statistics

---

## 🔴 Stop the Server

Press `Ctrl + C` in the terminal where the server is running.

Or kill the process:
```bash
# Find the process
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)
```

---

## 🐛 Troubleshooting

### **Port 5000 already in use**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Then start again
python3 app.py
```

### **Cannot access from other devices**
The server runs on `0.0.0.0:5000`, accessible from:
- **Local**: http://localhost:5000
- **Network**: http://YOUR_LOCAL_IP:5000

Find your IP:
```bash
hostname -I | awk '{print $1}'
```

### **Static files not loading**
Clear browser cache and refresh (Ctrl + Shift + R)

### **WebSocket connection fails**
Check browser console (F12) for errors.
Ensure Flask-SocketIO is installed:
```bash
pip show Flask-SocketIO
```

---

## 📱 Mobile Access

1. Find your computer's local IP:
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
```

2. On your mobile device, connect to the same WiFi

3. Open browser and navigate to:
```
http://YOUR_COMPUTER_IP:5000
```

---

## 🎨 Customizing the Frontend

### **Edit Templates**
```bash
nano app/views/templates/index.html
```

### **Edit Styles**
```bash
nano app/views/static/css/styles.css
```

### **Edit JavaScript**
```bash
nano app/views/static/js/main.js
```

Changes are reflected immediately (Flask auto-reloads in debug mode).

---

## 🚀 Production Deployment

For production, use a proper WSGI server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
```

---

## 📊 Development vs Production

### **Development (Current)**
```python
# In app.py
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

### **Production**
```bash
gunicorn --worker-class eventlet -w 1 app:app
```

---

## ✅ Ready to Start!

Run this command:
```bash
./start.sh
```

Or:
```bash
python3 app.py
```

Then open: **http://localhost:5000** 🎉
