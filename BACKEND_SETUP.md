# Backend Setup Guide - AI-Powered Smart Gym Trainer

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository
```bash
cd /home/nipho/Documents/AI-Powered-Smart-Gym-Trainer
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up PostgreSQL Database

**Create Database:**
```sql
CREATE DATABASE gym_trainer_db;
CREATE USER gym_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gym_trainer_db TO gym_user;
```

### 6. Configure Environment Variables

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://gym_user:your_password@localhost:5432/gym_trainer_db
SECRET_KEY=your-unique-secret-key
JWT_SECRET_KEY=your-unique-jwt-secret
FLASK_ENV=development
FLASK_DEBUG=True
```

**Generate secure secret keys:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 7. Initialize Database

The database tables will be created automatically when you run the application for the first time. Alternatively, you can use Flask-Migrate:

```bash
# Optional: Using Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 8. Run the Application

**Development Mode:**
```bash
python app.py
```

The server will start on `http://localhost:5000`

**Production Mode (using Gunicorn):**
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
```

## Project Structure

```
AI-Powered-Smart-Gym-Trainer/
├── app.py                          # Main application file
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .env.example                   # Environment variables template
├── API_DOCUMENTATION.md           # API documentation
├── app/
│   ├── __init__.py
│   ├── controllers/               # Business logic
│   │   ├── auth_controller.py    # Authentication logic
│   │   ├── workout_controller.py # Workout management logic
│   │   └── analytics_controller.py # Analytics logic
│   ├── models/                    # Database models
│   │   ├── __init__.py
│   │   ├── user_model.py         # User model
│   │   ├── workout_model.py      # Workout model
│   │   └── pose_detection.py     # Pose detection model
│   ├── routes/                    # API endpoints
│   │   ├── auth_routes.py        # Authentication routes
│   │   ├── workout.py            # Workout routes
│   │   └── analytics_routes.py   # Analytics routes
│   ├── utils/                     # Utility functions
│   │   ├── pose_utils.py         # Pose detection utilities
│   │   ├── posture_feedback.py   # Posture feedback
│   │   ├── camera_utils.py       # Camera utilities
│   │   └── data_utils.py         # Data validation utilities
│   └── views/                     # Frontend templates
│       ├── templates/             # HTML templates
│       └── static/                # CSS, JS files
```

## Features Implemented

### 1. Authentication System
- User registration with password hashing
- User login with JWT token generation
- Session management
- User profile management

### 2. Workout Management
- Log workouts (exercise, reps, sets)
- View workout history
- Update/delete workouts
- Filter workouts by exercise
- Calculate total reps

### 3. Real-Time Pose Detection
- MediaPipe integration for pose detection
- WebSocket connection for real-time video processing
- Bicep curl detection and counting
- Support for multiple exercises (squats, push-ups, shoulder press)

### 4. Analytics & Statistics
- Workout summary (total workouts, reps, sets)
- Exercise breakdown
- Progress tracking over time
- Recent activity
- Personal records
- Detailed exercise statistics

### 5. Data Utilities
- Input validation
- Email validation
- Password strength checking
- Data sanitization
- Response formatting

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/profile` - Get user profile

### Workouts
- `POST /workout/log` - Log workout
- `GET /workout/history` - Get workout history
- `GET /workout/<id>` - Get specific workout
- `PUT /workout/<id>` - Update workout
- `DELETE /workout/<id>` - Delete workout
- `GET /workout/exercise/<name>` - Get workouts by exercise
- `GET /workout/total-reps` - Get total reps

### Analytics
- `GET /analytics/summary` - Get workout summary
- `GET /analytics/breakdown` - Get exercise breakdown
- `GET /analytics/progress/<exercise>` - Get progress data
- `GET /analytics/recent` - Get recent activity
- `GET /analytics/records` - Get personal records
- `GET /analytics/exercise/<exercise>/stats` - Get exercise stats

### WebSocket Events
- `connect` - Client connection
- `frame` - Send video frame for processing
- `start_workout` - Start workout session
- `stop_workout` - Stop workout session

## Testing the API

### Using cURL

**Register User:**
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","password":"password123"}'
```

**Login:**
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}' \
  -c cookies.txt
```

**Log Workout:**
```bash
curl -X POST http://localhost:5000/workout/log \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"exercise":"Bicep Curl","reps":10,"sets":3}'
```

### Using Python

```python
import requests

# Register
response = requests.post('http://localhost:5000/auth/register', json={
    'name': 'John Doe',
    'email': 'john@example.com',
    'password': 'password123'
})
print(response.json())

# Login
response = requests.post('http://localhost:5000/auth/login', json={
    'email': 'john@example.com',
    'password': 'password123'
})
data = response.json()
session = requests.Session()
session.cookies.update(response.cookies)

# Log workout
response = session.post('http://localhost:5000/workout/log', json={
    'exercise': 'Bicep Curl',
    'reps': 10,
    'sets': 3
})
print(response.json())
```

## WebSocket Testing

```javascript
// Connect to WebSocket
const socket = io('http://localhost:5000');

// Listen for connection
socket.on('connection_response', (data) => {
    console.log('Connected:', data);
});

// Send video frame
socket.emit('frame', base64ImageData);

// Listen for response
socket.on('response', (data) => {
    console.log('Count:', data.count, 'Stage:', data.stage);
});
```

## Common Issues and Solutions

### Database Connection Error
**Error:** `could not connect to server`
**Solution:** Ensure PostgreSQL is running and DATABASE_URL is correct

### Module Not Found Error
**Error:** `ModuleNotFoundError: No module named 'flask'`
**Solution:** Activate virtual environment and install dependencies

### Port Already in Use
**Error:** `Address already in use`
**Solution:** 
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### WebSocket Connection Failed
**Error:** `WebSocket connection failed`
**Solution:** Ensure CORS is enabled and check firewall settings

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | PostgreSQL connection string | Yes | - |
| SECRET_KEY | Flask secret key | Yes | - |
| JWT_SECRET_KEY | JWT secret key | Yes | - |
| FLASK_ENV | Flask environment | No | development |
| FLASK_DEBUG | Enable debug mode | No | True |
| HOST | Server host | No | 0.0.0.0 |
| PORT | Server port | No | 5000 |
| MIN_DETECTION_CONFIDENCE | Pose detection confidence | No | 0.5 |
| MIN_TRACKING_CONFIDENCE | Pose tracking confidence | No | 0.5 |

## Next Steps

1. Test all API endpoints using Postman or cURL
2. Connect frontend to backend APIs
3. Test real-time pose detection with webcam
4. Add more exercises to pose detection
5. Implement workout recommendations
6. Add user authentication middleware
7. Deploy to production server

## Support

For issues or questions:
1. Check API_DOCUMENTATION.md for endpoint details
2. Review error logs in console
3. Verify environment variables are set correctly
4. Ensure all dependencies are installed

## License

This project is part of the AI-Powered Smart Gym Trainer system.
