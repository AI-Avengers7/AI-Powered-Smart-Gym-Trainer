from flask import Flask, render_template, request
from flask_socketio import SocketIO
import base64
import cv2
from app.routes.workout import process_frame
import numpy as np
import os
from config import config

app = Flask(__name__, static_folder=os.path.abspath('app/views/static'), template_folder=os.path.abspath('app/views/templates'))
app.secret_key = "test"
app.config.from_object(config)

socketio = SocketIO(app)

@app.route('/workout/')
def index():
    """Render the main page."""
    return render_template('workout.html')

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    print('Client disconnected')

@socketio.on('frame')
def handle_frame(data):
    """Handle incoming frames from the client."""

    user_id = request.sid
    try:
        # Decode the base64 image
        header, encoded = data.split(",", 1)
        binary_data = base64.b64decode(encoded)
        image_array = np.frombuffer(binary_data, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

      
        count, stage = process_frame(frame, user_id)

  
    
        socketio.emit('response', {'status': 'success', 'message': count})

    except Exception as e:
        print(f"Error processing frame: {e}")
        socketio.emit('response', {'status': 'error', 'message': str(e)})



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)