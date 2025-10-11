# Rep Counting Troubleshooting Guide

## Issue: Reps Not Counting During Workout

This guide will help you diagnose and fix rep counting issues.

---

## Quick Diagnostics

### 1. **Test Pose Detection Standalone**

Run the test script to verify MediaPipe is working:

```bash
python test_pose_detection.py
```

**Expected behavior:**
- You should see your camera feed with angles displayed
- Left and right elbow angles should update in real-time
- When you do a bicep curl, the count should increment
- Stage should change between "down" and "up"

**If the test works but the web app doesn't:**
- Issue is with the WebSocket communication or frontend integration
- Check browser console for errors
- Check server logs for frame processing

**If the test doesn't work:**
- MediaPipe may not be detecting your pose
- See "Common Pose Detection Issues" below

---

### 2. **Check Server Logs**

When running the Flask app, you should see these logs:

```
🆕 Initialized state for user <socket_id>
✅ Rep completed! User <socket_id>: Count=1, Angle=35
🏋️ User <socket_id>: Count=1, Stage=up
```

**If you don't see "Initialized state":**
- Frames are not reaching the backend
- Check WebSocket connection in browser console

**If you see "Initialized" but no "Rep completed":**
- Pose is not being detected OR
- Angles are not meeting thresholds
- Run the standalone test script to verify

---

### 3. **Check Browser Console**

Open Developer Tools (F12) and check for:

```javascript
📥 Server response: {status: "success", count: 1, stage: "up"}
🔢 Rep count updated: 1
📹 Sent 30 frames
```

**If you don't see "Server response":**
- WebSocket not connected
- Check connection status in UI
- Refresh page and check for Socket.IO errors

**If you see responses but count is always 0:**
- Backend is not detecting reps
- See "Common Pose Detection Issues" below

---

## Common Pose Detection Issues

### Issue 1: No Pose Detected

**Symptoms:**
- Test script shows "No pose detected"
- No angles displayed

**Solutions:**
1. **Improve lighting** - MediaPipe needs good lighting
2. **Move back from camera** - Your full upper body should be visible
3. **Check camera angle** - Face the camera directly
4. **Wear contrasting clothing** - Helps with detection
5. **Clear background** - Reduces false detections

### Issue 2: Angles Not Meeting Thresholds

**Symptoms:**
- Angles are displayed but count doesn't increment
- Stage doesn't change

**Current thresholds:**
- **DOWN position**: Angle > 160° (arm extended)
- **UP position**: Angle < 40° (arm curled)

**Solutions:**

1. **Adjust thresholds** in `app/routes/workout.py`:
   ```python
   # Try more lenient thresholds
   if angle > 150:  # was 160
       state['stage'] = 'down'
   elif angle < 50:  # was 40
       # count rep
   ```

2. **Perform full range of motion:**
   - Extend arm completely for DOWN (should be ~180°)
   - Curl completely for UP (should be ~30°)

3. **Try different arm:**
   - Code uses the minimum angle of both arms
   - Make sure you're moving the arm that's visible to camera

### Issue 3: Premature Counting

**Symptoms:**
- Count increments too quickly
- Multiple reps counted for one movement

**Solutions:**

Add a cooldown period in `app/routes/workout.py`:
```python
import time

def process_frame(frame, user_id):
    if user_id not in user_states:
        user_states[user_id] = {
            'count': 0, 
            'stage': 'ready', 
            'last_rep_time': 0
        }
    
    state = user_states[user_id]
    current_time = time.time()
    
    # ... detection code ...
    
    # Only count if at least 1 second has passed
    if angle < 40 and state['stage'] == 'down':
        if current_time - state['last_rep_time'] > 1.0:
            state['stage'] = 'up'
            state['count'] += 1
            state['last_rep_time'] = current_time
```

---

## Verify Installation

Check that all dependencies are installed correctly:

```bash
# Activate virtual environment
source venv/bin/activate

# Verify installations
python -c "import mediapipe; print(f'MediaPipe: {mediapipe.__version__}')"
python -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
```

**Expected output:**
```
MediaPipe: 0.10.21
OpenCV: 4.8.1
NumPy: 1.24.x
```

If any import fails, reinstall:
```bash
pip install --force-reinstall mediapipe opencv-python numpy
```

---

## WebSocket Connection Issues

### Verify WebSocket is Connected

Check browser console for:
```
✅ Connected to server
```

If you see disconnection errors:

1. **Check CORS settings** in `app.py`:
   ```python
   socketio = SocketIO(app, cors_allowed_origins="*")
   ```

2. **Verify Socket.IO versions match:**
   - Backend: `Flask-SocketIO==5.3.6`
   - Frontend: Uses Socket.IO client from CDN

3. **Check firewall/network:**
   - Make sure port 5000 is not blocked
   - Try accessing from `localhost` instead of IP address

---

## Frontend Issues

### Count Not Updating in UI

If backend logs show count incrementing but UI doesn't update:

1. **Check `workout.js` event handler:**
   ```javascript
   socket.on('response', function(data) {
       console.log('📥 Server response:', data);
       if (data.count !== undefined) {
           const repCounter = document.getElementById('repCounter');
           repCounter.textContent = data.count;
       }
   });
   ```

2. **Verify element IDs exist:**
   ```bash
   grep -n "id=\"repCounter\"" app/views/templates/workout.html
   grep -n "id=\"repStage\"" app/views/templates/workout.html
   ```

3. **Hard refresh the page:** Ctrl+Shift+R (clears cache)

---

## Performance Optimization

If frames are processing slowly:

1. **Reduce frame rate** in `workout.js`:
   ```javascript
   // Send frames every 200ms instead of 100ms
   frameInterval = setInterval(() => {
       sendFrame();
   }, 200);
   ```

2. **Lower video resolution:**
   ```javascript
   navigator.mediaDevices.getUserMedia({ 
       video: { 
           width: 640,  // Lower from 1280
           height: 480   // Lower from 720
       } 
   })
   ```

3. **Reduce MediaPipe confidence:**
   In `pose_utils.py`:
   ```python
   mp_pose.Pose(
       min_detection_confidence=0.3,  # Lower from 0.5
       min_tracking_confidence=0.3
   )
   ```

---

## Testing Checklist

Before reporting an issue, verify:

- [ ] Virtual environment is activated
- [ ] All dependencies installed (`pip list | grep -i mediapipe`)
- [ ] Camera permissions granted in browser
- [ ] Good lighting in room
- [ ] Full upper body visible in camera
- [ ] Standalone test script works (`python test_pose_detection.py`)
- [ ] WebSocket connected (check browser console)
- [ ] Server running without errors
- [ ] Browser console shows frame being sent
- [ ] Server logs show frames being received
- [ ] Performing full range of motion for exercise

---

## Still Not Working?

1. **Capture diagnostic info:**
   ```bash
   # Run test script and save output
   python test_pose_detection.py > pose_test.log 2>&1
   
   # Check server logs
   python app.py > server.log 2>&1
   ```

2. **Check the logs for:**
   - Detected angles (should range from ~30° to ~180°)
   - Stage transitions (down → up)
   - Error messages from MediaPipe

3. **Try a different exercise:**
   - Squats or shoulder press may work better
   - Update detection logic in `process_frame` accordingly

4. **Verify camera works:**
   ```bash
   # Simple OpenCV camera test
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAIL')"
   ```

---

## Exercise-Specific Detection

Currently only **bicep curls** are implemented. For other exercises:

### Squats
```python
# In process_frame, use hip-knee-ankle angle
def detect_squat(landmarks):
    left_hip = [landmarks.landmark[23].x, landmarks.landmark[23].y]
    left_knee = [landmarks.landmark[25].x, landmarks.landmark[25].y]
    left_ankle = [landmarks.landmark[27].x, landmarks.landmark[27].y]
    
    angle = calculate_angle(left_hip, left_knee, left_ankle)
    return angle
```

- DOWN: angle < 90° (squatting)
- UP: angle > 160° (standing)

### Push-ups
```python
# Use shoulder-elbow-wrist angle
def detect_pushup(landmarks):
    # Similar to bicep_curl but check if person is horizontal
    # You may need to check shoulder-hip alignment too
```

---

## Contact & Support

If issues persist:
1. Check the logs in `server.log` and `pose_test.log`
2. Review error messages in browser console
3. Verify all dependencies are correctly installed
4. Test with the standalone pose detection script first
