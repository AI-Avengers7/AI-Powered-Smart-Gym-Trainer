# Rep Counting Debug Summary

## What We've Done

### 1. **Enhanced Backend Logging**
   - Added detailed logging to `app.py` handle_frame function
   - Added logging to `process_frame` in workout routes
   - Now tracks when reps are completed with angle information

### 2. **Improved Rep Counting Logic**
   - Modified `process_frame` function with better state management
   - Changed angle thresholds:
     - DOWN: angle > 160° (arm extended)
     - UP: angle < 40° (arm curled) + previous stage was "down"
     - MIDDLE: 40° ≤ angle ≤ 160° (transition zone)
   - Uses minimum angle of both arms (whichever arm is being used)
   - Added "ready" state for initialization

### 3. **Created Test Script**
   - `test_pose_detection.py` - Standalone camera test
   - Shows real-time angles and rep counting
   - Verifies MediaPipe pose detection works independently
   - **Currently running** - You should see a camera window with angle overlays

### 4. **Created Troubleshooting Guide**
   - `REP_COUNTING_TROUBLESHOOTING.md` - Comprehensive debug guide
   - Covers common issues and solutions
   - Step-by-step diagnostic procedures

---

## How to Test

### Test 1: Standalone Pose Detection (RUNNING NOW)

The test script should show a window with your camera feed. You should see:
- "Left Angle: X" and "Right Angle: X" displayed
- "Stage: down/up/ready" 
- "Count: X" that increments when you do bicep curls

**To test:**
1. Stand back so your full upper body is visible
2. Face the camera directly
3. Do a bicep curl:
   - Start with arm extended down (should show ~180°)
   - Curl arm up completely (should show ~30°)
   - Extend back down
4. Count should increment when you complete the curl

**Press 'Q' to quit the test**

---

### Test 2: Web Application

After verifying the standalone test works:

1. **Start the server:**
   ```bash
   cd /home/nipho/Documents/AI-Powered-Smart-Gym-Trainer
   source venv/bin/activate
   python app.py
   ```

2. **Open browser** to http://localhost:5000

3. **Navigate to Workout page**

4. **Click "Start Camera"**

5. **Select "Bicep Curls" from dropdown**

6. **Click "Start Exercise"**

7. **Perform bicep curls** (same as in standalone test)

8. **Watch the logs** in terminal for:
   ```
   🆕 Initialized state for user <socket_id>
   ✅ Rep completed! User <socket_id>: Count=1, Angle=35
   🏋️ User <socket_id>: Count=1, Stage=up
   ```

9. **Check browser console** (F12) for:
   ```
   📥 Server response: {count: 1, stage: "up"}
   🔢 Rep count updated: 1
   ```

10. **Watch the UI** - Rep counter should increment

---

## Expected Behavior

### When Pose is NOT Detected:
- **Standalone test**: Shows "No pose detected - move into frame"
- **Web app**: Count stays at 0, no stage changes
- **Server logs**: No "Rep completed" messages

### When Pose IS Detected but No Reps:
- **Standalone test**: Shows angles updating in real-time
- **Web app**: You see yourself in camera feed
- **Server logs**: Shows initialized state
- **Issue**: Angles may not be reaching thresholds

### When Everything Works:
- **Standalone test**: Count increments, stage changes down→up
- **Web app**: UI updates, rep counter increases
- **Server logs**: Shows "✅ Rep completed!" messages
- **Browser console**: Shows updated count in responses

---

## Common Issues & Solutions

### Issue: "No pose detected"
**Cause**: MediaPipe can't see your body clearly

**Solutions:**
1. Improve lighting (turn on more lights)
2. Move back from camera (full upper body visible)
3. Face camera directly
4. Wear contrasting clothing
5. Clear background behind you

---

### Issue: Angles show but count doesn't increase
**Cause**: Angles not reaching thresholds (160° down, 40° up)

**Solutions:**
1. Do FULL range of motion:
   - Extend arm completely (should reach ~180°)
   - Curl completely (should reach ~30°)
2. Watch the angle numbers in test window
3. Adjust thresholds if needed (see troubleshooting guide)
4. Make sure the arm you're using is clearly visible

---

### Issue: Test works but web app doesn't
**Cause**: WebSocket communication issue

**Solutions:**
1. Check browser console for connection errors
2. Verify server is running without errors
3. Hard refresh page (Ctrl+Shift+R)
4. Check that frames are being sent (look for "📹" logs)

---

### Issue: Count increments too fast
**Cause**: Multiple detections for single rep

**Solution:** Add cooldown period (see troubleshooting guide)

---

## Key Code Changes

### app/routes/workout.py
```python
def process_frame(frame, user_id):
    # Initialize with 'ready' stage
    if user_id not in user_states:
        user_states[user_id] = {'count': 0, 'stage': 'ready', 'last_count': 0}
        print(f"🆕 Initialized state for user {user_id}")
    
    # Use minimum angle (the arm being used)
    angle = min(l_angle, r_angle)
    
    # Better threshold logic
    if angle > 160:
        state['stage'] = 'down'
    elif angle < 40 and state['stage'] == 'down':
        state['stage'] = 'up'
        state['count'] += 1
        print(f"✅ Rep completed! User {user_id}: Count={state['count']}, Angle={angle}")
```

### app.py
```python
@socketio.on('frame')
def handle_frame(data):
    # Process and log rep counting
    count, stage = process_frame(frame, user_id)
    
    # Log every 5th frame or when rep completed
    if count % 5 == 0 or stage == 'up':
        print(f"🏋️ User {user_id}: Count={count}, Stage={stage}")
```

---

## Next Steps

1. **Check the test window** that should be open now
   - Is your pose being detected?
   - Are angles showing?
   - Does count increment when you do bicep curls?

2. **If test works**, try the web app and compare behavior

3. **If test doesn't work**, follow troubleshooting guide to:
   - Improve lighting/positioning
   - Verify MediaPipe installation
   - Adjust angle thresholds

4. **Review server logs** to see exactly what's happening during workout

---

## Files Modified

- ✅ `app.py` - Enhanced logging in handle_frame
- ✅ `app/routes/workout.py` - Improved process_frame logic
- ✅ `test_pose_detection.py` - Created standalone test
- ✅ `REP_COUNTING_TROUBLESHOOTING.md` - Comprehensive guide

---

## What to Check Right Now

Look at the test window that's running. It should show:
1. Your camera feed
2. Detected angles in green text (top left)
3. Current stage and count
4. Colored bar at top (red=down, green=up)

**Try doing one bicep curl and observe:**
- Does the angle change from ~180° to ~30°?
- Does the stage change from "down" to "up"?
- Does the count increment?

If YES → Great! MediaPipe is working. Issue is with web app integration.
If NO → Follow the "No pose detected" or "Angles not reaching thresholds" solutions above.

**Press Q to close the test window when done.**
