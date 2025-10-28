# Project Overview

This project is an AI-Powered Smart Gym Trainer. It uses a Flask backend and a React frontend. The backend uses computer vision with MediaPipe to analyze user's workout form in real-time, count repetitions, and provide feedback. The frontend is a web application that displays the real-time feedback and workout analytics.

## Building and Running

### Backend

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the server:**
    ```bash
    python app.py
    ```

The backend will be running on `http://localhost:5000`.

### Frontend

1.  **Install dependencies:**
    ```bash
    cd frontend
    npm install
    ```

2.  **Run the development server:**
    ```bash
    npm run dev
    ```

The frontend will be running on `http://localhost:5173`.

## Development Conventions

*   **Backend:** The backend is written in Python using Flask. It follows a modular structure with Blueprints for different functionalities. It uses SQLAlchemy as an ORM for database interactions.
*   **Frontend:** The frontend is a React application written in TypeScript. It uses Vite for building and development. It also uses Tailwind CSS for styling.
*   **Real-time Communication:** The frontend and backend communicate in real-time using WebSockets (Flask-SocketIO).
*   **Authentication:** The application uses JSON Web Tokens (JWT) for authentication.
