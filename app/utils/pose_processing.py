"""
Pose Processing Utilities
"""
from app.utils.pose_utils import detect_pose, bicep_curl

# Store user states for real-time tracking
user_states = {}

def process_frame(frame, user_id):
    """
    Process a frame to detect bicep curls and update the user's state.
    
    Args:
        frame: Video frame to process
        user_id: ID of the user
        
    Returns:
        tuple: (count, stage)
    """
    # Initialize user state if it doesn't exist
    if user_id not in user_states:
        user_states[user_id] = {'count': 0, 'stage': 'ready', 'last_count': 0}
        print(f"🆕 Initialized state for user {user_id}")

    # Get the user's state
    state = user_states[user_id]

    # Check if the frame is valid
    if frame is None:
        return state['count'], state['stage']

    # Detect landmarks
    landmarks = detect_pose(frame)

    # Check if landmarks are detected
    if landmarks is None:
        # No pose detected, keep current state
        return state['count'], state.get('stage', 'ready')

    # Calculate bicep curl angles
    l_angle, r_angle = bicep_curl(landmarks)

    # Check if angles are valid
    if l_angle is None or r_angle is None:
        return state['count'], state.get('stage', 'ready')

    # Use the smaller angle (the arm being used)
    angle = min(l_angle, r_angle)

    # Adjusted thresholds for better detection:
    # DOWN position: arm is mostly extended (more forgiving)
    DOWN_THRESHOLD = 140
    # UP position: arm is well curled (more achievable)
    UP_THRESHOLD = 50
    # Middle range boundaries
    MIDDLE_LOW = 70
    MIDDLE_HIGH = 120

    # Update stage and count based on angle
    # DOWN position: arm is extended (angle > 140°)
    if angle > DOWN_THRESHOLD:
        if state['stage'] != 'down':
            state['stage'] = 'down'
            print(f"⬇️  User {user_id}: DOWN position (angle={angle:.1f}°)")
            
    # UP position: arm is curled (angle < 50°)
    elif angle < UP_THRESHOLD:
        if state['stage'] == 'down':
            # Just completed a rep!
            state['stage'] = 'up'
            state['count'] += 1
            print(f"✅ REP COMPLETED! User {user_id}: Count={state['count']}, Angle={angle:.1f}°")
        elif state['stage'] != 'up':
            state['stage'] = 'up'
            print(f"⬆️  User {user_id}: UP position (angle={angle:.1f}°)")
    
    # MIDDLE position - transitioning
    elif UP_THRESHOLD <= angle <= DOWN_THRESHOLD:
        # In the middle range - moving between positions
        if state['stage'] == 'up' and angle > MIDDLE_HIGH:
            # Coming down from curled position
            state['stage'] = 'lowering'
            print(f"↘️  User {user_id}: Lowering arm (angle={angle:.1f}°)")
        elif state['stage'] == 'down' and angle < MIDDLE_LOW:
            # Coming up from extended position  
            state['stage'] = 'raising'
            print(f"↗️  User {user_id}: Raising arm (angle={angle:.1f}°)")
        elif state['stage'] == 'lowering' and angle > DOWN_THRESHOLD:
            # Reached down position from lowering
            state['stage'] = 'down'

    return state['count'], state['stage']
