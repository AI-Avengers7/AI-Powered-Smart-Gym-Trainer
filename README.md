# AI-Powered Smart Gym Trainer

The **AI-Powered Smart Gym Trainer** is a software-based system designed to provide real-time feedback and guidance to users during their workouts. It uses AI pose detection to analyze exercise form, count repetitions, and provide corrective feedback. The system is accessible via a web app, making it easy to use on any device with a webcam.

## Project Overview

This project aims to help fitness enthusiasts, beginners, and gym owners/trainers improve workout efficiency and safety through AI-powered real-time feedback. By analyzing user movements with pose detection technology, the system provides detailed guidance on posture, helps count repetitions, and offers personalized workout suggestions.

## Key Features

- **Pose Detection**: 
    - Detect key body landmarks (e.g., joints, limbs) using AI models like OpenPose or MediaPipe.
    - Monitor exercises such as squats, push-ups, deadlifts, etc.
  
- **Real-Time Feedback**:
    - Provide immediate feedback on posture and form (e.g., "Keep your back straight during squats").
    - Highlight incorrect movements and suggest corrections.

- **Rep Counting**:
    - Automatically count repetitions for each exercise.
    - Track the start and end positions of movements to ensure accuracy.

- **Workout Logging**:
    - Store workout data (e.g., sets, reps, feedback) in a database.
    - Allow users to view their workout history and track progress over time.

- **Personalized Suggestions**:
    - Recommend exercises or adjustments based on user performance.
    - Adjust workout difficulty based on user progress.

- **Workout Analytics**:
    - Display progress through charts, graphs, and logs.
    - Provide metrics such as posture accuracy, strength improvements, and calories burned.

- **User-Friendly Interface**:
    - A responsive web app accessible on both desktop and mobile devices.
    - Interactive dashboard for viewing feedback, progress, and suggestions.

## Technology Stack

- **Frontend**: Vanilla HTML, JavaScript, and Tailwind CSS (for styling)
- **Backend**: Flask (for the RESTful API)
- **AI Pose Detection**: OpenPose or MediaPipe (for analyzing user movements)
- **Camera**: Standard webcam or external USB camera
- **Database**: SQLite, PostgreSQL, or MongoDB (for storing user data)
- **Libraries**:
    - OpenCV (for capturing and processing video frames)
    - WebSocket or HTTP requests (for real-time communication between frontend and backend)
    - Chart.js or D3.js (for displaying workout analytics)

## Installation

### Prerequisites

- Python 3.x and pip installed for backend development
- Virtual environment (recommended for Python dependencies)

### Frontend Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/smart-gym-trainer.git
    cd smart-gym-trainer/frontend
    ```

2. Add Tailwind CSS to your project:
    - You can either add Tailwind via a CDN directly into your HTML files or install it manually.

    **Using Tailwind via CDN:**
    In the `<head>` section of your `index.html`, add:
    ```html
    <script src="https://cdn.tailwindcss.com"></script>
    ```

    **Manually adding Tailwind (Optional)**:
    - Download Tailwind's CSS file and include it in your HTML by linking to it in the `<head>` section:
    ```html
    <link href="path/to/tailwind.css" rel="stylesheet">
    ```

3. Open the `index.html` file in your browser to view the frontend.

### Backend Setup

1. Navigate to the backend folder:
    ```bash
    cd smart-gym-trainer/backend
    ```

2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask server:
    ```bash
    python app.py
    ```
   The backend will be running on `http://localhost:5000`.

### AI Pose Detection Setup

1. Install the necessary libraries for OpenPose or MediaPipe, depending on your choice. For example, to use MediaPipe:
    ```bash
    pip install mediapipe
    ```

2. Configure the camera feed to work with the AI pose detection system. This will be part of the backend processing.

## How It Works

1. **Camera Setup**:
    - A webcam or external camera captures the user’s movements during exercises.
    - The video feed is sent to the AI model running on the backend for pose detection.

2. **AI Pose Detection**:
    - OpenPose or MediaPipe analyzes the video feed to detect key body landmarks.
    - The system extracts pose data (e.g., joint angles) to evaluate exercise form.

3. **Real-Time Feedback**:
    - The backend processes the pose data and provides feedback on posture and form.
    - Feedback is displayed on the web app in real-time.

4. **Workout Logging**:
    - The backend stores workout data (e.g., reps, sets, feedback) in a database.
    - Users can view their workout history and progress through the web app.

5. **Personalized Suggestions**:
    - Based on user performance, the system suggests exercises or adjustments to improve results.

## Testing and Deployment

1. **Testing**:
    - Test the AI model with different exercises, body types, and lighting conditions to ensure accurate pose detection.
    - Validate the real-time feedback feature under various workout scenarios.

2. **Deployment**:
    - Deploy the frontend as a static website by uploading the `frontend` folder to platforms like GitHub Pages, Netlify, or any static file hosting service.
    - Deploy the backend on platforms like Heroku, AWS, or any other cloud-based service that supports Flask apps.

## Future Enhancements

- Add support for more exercises and advanced workout routines.
- Integrate wearable devices for additional data (e.g., heart rate, calories burned).
- Develop a mobile app for on-the-go access.
- Implement gamification features (e.g., badges, challenges) to motivate users.

## Potential Challenges

- **Computational Requirements**: OpenPose and similar models can be resource-intensive and may require powerful hardware for smooth performance.
- **Lighting and Background Conditions**: Pose detection accuracy can be affected by varying lighting or background clutter.
- **Real-Time Performance**: Ensuring low latency for real-time feedback may require optimization of backend systems and network performance.

