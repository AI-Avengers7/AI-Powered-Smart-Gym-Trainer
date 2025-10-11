# API Documentation - AI-Powered Smart Gym Trainer

## Base URL
```
http://localhost:5000
```

## Authentication Routes

### Register User
- **Endpoint:** `/auth/register`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully"
}
```

---

### Login User
- **Endpoint:** `/auth/login`
- **Method:** `POST`
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Logout User
- **Endpoint:** `/auth/logout`
- **Method:** `POST`

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

### Get User Profile
- **Endpoint:** `/auth/profile`
- **Method:** `GET`
- **Authentication:** Required (Session)

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

## Workout Routes

### Log Workout
- **Endpoint:** `/workout/log`
- **Method:** `POST`
- **Authentication:** Required
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "exercise": "Bicep Curl",
  "reps": 10,
  "sets": 3,
  "feedback": "Good form"
}
```

**Response (201 Created):**
```json
{
  "message": "Workout logged successfully",
  "workout": {
    "id": 1,
    "exercise": "Bicep Curl",
    "reps": 10,
    "sets": 3
  }
}
```

---

### Get Workout History
- **Endpoint:** `/workout/history`
- **Method:** `GET`
- **Authentication:** Required
- **Query Parameters:** `limit` (optional)

**Example:** `/workout/history?limit=10`

**Response (200 OK):**
```json
{
  "workouts": [
    {
      "id": 1,
      "exercise": "Bicep Curl",
      "reps": 10,
      "sets": 3,
      "user_id": 1
    }
  ],
  "count": 1
}
```

---

### Get Specific Workout
- **Endpoint:** `/workout/<workout_id>`
- **Method:** `GET`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "id": 1,
  "exercise": "Bicep Curl",
  "reps": 10,
  "sets": 3,
  "user_id": 1
}
```

---

### Update Workout
- **Endpoint:** `/workout/<workout_id>`
- **Method:** `PUT`
- **Authentication:** Required
- **Content-Type:** `application/json`

**Request Body:**
```json
{
  "exercise": "Push Up",
  "reps": 15,
  "sets": 4
}
```

**Response (200 OK):**
```json
{
  "message": "Workout updated successfully"
}
```

---

### Delete Workout
- **Endpoint:** `/workout/<workout_id>`
- **Method:** `DELETE`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "message": "Workout deleted successfully"
}
```

---

### Get Workouts by Exercise
- **Endpoint:** `/workout/exercise/<exercise_name>`
- **Method:** `GET`
- **Authentication:** Required

**Example:** `/workout/exercise/Bicep%20Curl`

**Response (200 OK):**
```json
{
  "exercise": "Bicep Curl",
  "workouts": [
    {
      "id": 1,
      "exercise": "Bicep Curl",
      "reps": 10,
      "sets": 3
    }
  ],
  "count": 1
}
```

---

### Get Total Reps
- **Endpoint:** `/workout/total-reps`
- **Method:** `GET`
- **Authentication:** Required
- **Query Parameters:** `exercise` (optional)

**Example:** `/workout/total-reps?exercise=Bicep%20Curl`

**Response (200 OK):**
```json
{
  "total_reps": 30,
  "exercise": "Bicep Curl",
  "workout_count": 1
}
```

---

### Reset Rep Count
- **Endpoint:** `/workout/reset-count`
- **Method:** `POST`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "message": "Count reset successfully"
}
```

---

## Analytics Routes

### Get Workout Summary
- **Endpoint:** `/analytics/summary`
- **Method:** `GET`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "total_workouts": 10,
  "total_reps": 150,
  "total_sets": 30,
  "exercises_performed": 3,
  "exercises": ["Bicep Curl", "Push Up", "Squat"]
}
```

---

### Get Exercise Breakdown
- **Endpoint:** `/analytics/breakdown`
- **Method:** `GET`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "breakdown": [
    {
      "exercise": "Bicep Curl",
      "workout_count": 5,
      "total_reps": 50,
      "total_sets": 15,
      "avg_reps_per_workout": 10.0
    }
  ]
}
```

---

### Get Progress Data
- **Endpoint:** `/analytics/progress/<exercise_name>`
- **Method:** `GET`
- **Authentication:** Required

**Example:** `/analytics/progress/Bicep%20Curl`

**Response (200 OK):**
```json
{
  "exercise": "Bicep Curl",
  "progress": [
    {
      "session": 1,
      "workout_id": 1,
      "reps": 10,
      "sets": 3,
      "total_reps": 30
    }
  ],
  "total_sessions": 1
}
```

---

### Get Recent Activity
- **Endpoint:** `/analytics/recent`
- **Method:** `GET`
- **Authentication:** Required
- **Query Parameters:** `limit` (optional, default: 10)

**Response (200 OK):**
```json
{
  "recent_activity": [
    {
      "id": 1,
      "exercise": "Bicep Curl",
      "reps": 10,
      "sets": 3,
      "total_reps": 30
    }
  ]
}
```

---

### Get Personal Records
- **Endpoint:** `/analytics/records`
- **Method:** `GET`
- **Authentication:** Required

**Response (200 OK):**
```json
{
  "personal_records": [
    {
      "exercise": "Bicep Curl",
      "max_reps": 15,
      "max_sets": 5,
      "max_total_reps": 75
    }
  ]
}
```

---

### Get Exercise Statistics
- **Endpoint:** `/analytics/exercise/<exercise_name>/stats`
- **Method:** `GET`
- **Authentication:** Required

**Example:** `/analytics/exercise/Bicep%20Curl/stats`

**Response (200 OK):**
```json
{
  "exercise": "Bicep Curl",
  "stats": {
    "total_sessions": 5,
    "total_reps": 150,
    "avg_reps": 30.0,
    "max_reps": 40,
    "total_sets": 15,
    "avg_sets": 3.0,
    "max_sets": 5
  }
}
```

---

## WebSocket Events

### Connect
- **Event:** `connect`
- **Description:** Client connects to WebSocket server

**Server Response:**
```json
{
  "status": "success",
  "message": "Connected to AI Gym Trainer",
  "session_id": "unique-session-id"
}
```

---

### Frame Processing
- **Event:** `frame`
- **Description:** Send video frame for real-time pose detection
- **Data:** Base64 encoded image

**Client Sends:**
```javascript
socket.emit('frame', base64ImageData);
```

**Server Response:**
```json
{
  "status": "success",
  "count": 5,
  "stage": "up"
}
```

---

### Start Workout
- **Event:** `start_workout`
- **Description:** Notify server that workout has started

**Client Sends:**
```json
{
  "exercise": "Bicep Curl"
}
```

**Server Response:**
```json
{
  "status": "success",
  "exercise": "Bicep Curl",
  "message": "Started Bicep Curl workout"
}
```

---

### Stop Workout
- **Event:** `stop_workout`
- **Description:** Notify server that workout has stopped

**Server Response:**
```json
{
  "status": "success",
  "message": "Workout stopped"
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

**Error Response:**
```json
{
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `500 Internal Server Error` - Server error

---

## Notes

1. All authenticated endpoints require either a valid session cookie or JWT token in the Authorization header
2. JWT tokens should be sent as: `Authorization: Bearer <token>`
3. WebSocket connections use Socket.IO protocol
4. All timestamps are in UTC
5. Exercise names are case-insensitive when querying
6. Base64 image data for frame processing should include the data URI prefix: `data:image/jpeg;base64,`
