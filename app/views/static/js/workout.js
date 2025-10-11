console.log('🏋️ Loading workout.js...');

// Get all DOM elements
const videoElement = document.getElementById('video');
const startCameraBtn = document.getElementById('startCamera');
const stopCameraBtn = document.getElementById('stopCamera');
const startExerciseBtn = document.getElementById('startExercise');
const endExerciseBtn = document.getElementById('endExercise');
const exerciseSelect = document.getElementById('exerciseSelect');
const repCounter = document.getElementById('repCounter');
const repStage = document.getElementById('repStage');
const totalRepsDisplay = document.getElementById('totalReps');
const sessionDurationDisplay = document.getElementById('sessionDuration');
const caloriesDisplay = document.getElementById('calories');
const cameraStatus = document.getElementById('cameraStatus');
const postureOverlay = document.getElementById('postureOverlay');
const postureText = document.getElementById('postureText');
const formFeedback = document.getElementById('formFeedback');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

console.log('Elements loaded:', {
    video: !!videoElement,
    startCamera: !!startCameraBtn,
    stopCamera: !!stopCameraBtn,
    startExercise: !!startExerciseBtn,
    endExercise: !!endExerciseBtn,
    repCounter: !!repCounter
});

let mediaStream = null;
let socket = null;
let isExercising = false;
let currentReps = 0;
let sessionStartTime = null;
let durationInterval = null;
let videoWidth = 640;
let videoHeight = 480;


const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

// Initialize Socket.IO connection
function initializeSocket() {
    console.log('Initializing socket connection...');
    socket = io('http://localhost:5000');
    
    socket.on('connect', () => {
        console.log('✅ Connected to server');
        if (statusIndicator) {
            statusIndicator.className = 'w-3 h-3 bg-green-500 rounded-full pulse-green';
        }
        if (statusText) {
            statusText.textContent = 'Connected';
            statusText.className = 'text-green-400 text-sm font-semibold';
        }
    });
    
    socket.on('disconnect', () => {
        console.log('❌ Disconnected from server');
        if (statusIndicator) {
            statusIndicator.className = 'w-3 h-3 bg-red-500 rounded-full';
        }
        if (statusText) {
            statusText.textContent = 'Disconnected';
            statusText.className = 'text-gray-400 text-sm';
        }
    });
    
    socket.on('response', (data) => {
        console.log('📥 Server response:', data);
        
        // Update rep counter
        if (data.count !== undefined && data.count !== currentReps) {
            currentReps = data.count;
            console.log('🔢 Rep count updated:', currentReps);
            
            if (repCounter) {
                repCounter.textContent = currentReps;
                repCounter.classList.add('shake');
                setTimeout(() => repCounter.classList.remove('shake'), 300);
            }
            
            if (totalRepsDisplay) {
                totalRepsDisplay.textContent = currentReps;
            }
            
            if (caloriesDisplay) {
                caloriesDisplay.textContent = Math.round(currentReps * 0.5);
            }
        }
        
        // Update stage
        if (data.stage && repStage) {
            const stages = {
                'up': '⬆️ Up',
                'down': '⬇️ Down',
                'ready': '✋ Ready'
            };
            repStage.textContent = stages[data.stage] || data.stage;
            
            if (data.stage === 'up') {
                repStage.className = 'text-green-400 text-lg font-semibold';
            } else if (data.stage === 'down') {
                repStage.className = 'text-blue-400 text-lg font-semibold';
            }
        }
        
        // Show posture feedback
        if (data.feedback && postureOverlay && postureText) {
            postureText.textContent = data.feedback;
            postureOverlay.classList.remove('hidden');
            setTimeout(() => postureOverlay.classList.add('hidden'), 3000);
        }
    });
    
    socket.on('error', (error) => {
        console.error('Socket.IO Error:', error);
    });
}

// Start Camera Button
if (startCameraBtn) {
    startCameraBtn.addEventListener('click', async () => {
        console.log('📷 Start Camera button clicked!');
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: videoWidth },
                    height: { ideal: videoHeight }
                } 
            });

            videoElement.srcObject = mediaStream;
            
            // Update UI
            startCameraBtn.classList.add('hidden');
            if (stopCameraBtn) stopCameraBtn.classList.remove('hidden');
            if (cameraStatus) {
                cameraStatus.textContent = '📷 Camera On';
                cameraStatus.className = 'absolute top-4 left-4 bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold pulse-green';
            }
            
            // Initialize socket
            if (!socket) {
                initializeSocket();
            }
            
            console.log('✅ Camera started successfully');
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            alert('Could not access camera. Please check permissions.');
        }
    });
}

// Stop Camera Button
if (stopCameraBtn) {
    stopCameraBtn.addEventListener('click', () => {
        console.log('⏹️ Stop Camera button clicked!');
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
        }
        
        stopCameraBtn.classList.add('hidden');
        if (startCameraBtn) startCameraBtn.classList.remove('hidden');
        if (cameraStatus) {
            cameraStatus.textContent = '📷 Camera Off';
            cameraStatus.className = 'absolute top-4 left-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold';
        }
    });
}

// Start Exercise Button
if (startExerciseBtn) {
    startExerciseBtn.addEventListener('click', () => {
        console.log('▶️ Start Exercise button clicked!');
        
        if (!mediaStream) {
            alert('Please start camera first!');
            return;
        }
        
        if (!socket || !socket.connected) {
            alert('Not connected to server! Please wait...');
            return;
        }
        
        isExercising = true;
        currentReps = 0;
        sessionStartTime = Date.now();
        
        // Update UI
        startExerciseBtn.classList.add('hidden');
        if (endExerciseBtn) endExerciseBtn.classList.remove('hidden');
        if (repCounter) repCounter.textContent = '0';
        if (repStage) repStage.textContent = 'Starting...';
        
        // Start duration timer
        durationInterval = setInterval(() => {
            if (sessionStartTime && sessionDurationDisplay) {
                const elapsed = Math.floor((Date.now() - sessionStartTime) / 1000);
                const minutes = Math.floor(elapsed / 60);
                const seconds = elapsed % 60;
                sessionDurationDisplay.textContent = 
                    `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
        }, 1000);
        
        // Notify server
        const exercise = exerciseSelect ? exerciseSelect.value : 'bicep_curl';
        socket.emit('start_workout', { exercise });
        
        // Start streaming
        startStreamingFrames();
        
        console.log('✅ Exercise started');
    });
}

// End Exercise Button
if (endExerciseBtn) {
    endExerciseBtn.addEventListener('click', () => {
        console.log('⏸️ End Exercise button clicked!');
        
        isExercising = false;
        
        // Update UI
        endExerciseBtn.classList.add('hidden');
        if (startExerciseBtn) startExerciseBtn.classList.remove('hidden');
        if (repStage) repStage.textContent = 'Finished';
        
        // Stop timer
        if (durationInterval) {
            clearInterval(durationInterval);
            durationInterval = null;
        }
        
        // Notify server
        if (socket) {
            const exercise = exerciseSelect ? exerciseSelect.value : 'bicep_curl';
            socket.emit('stop_workout', { 
                total_reps: currentReps,
                exercise: exercise
            });
        }
        
        console.log(`✅ Exercise ended. Total reps: ${currentReps}`);
        alert(`Session completed! Total reps: ${currentReps}`);
    });
}

function startStreamingFrames() {
    if (!mediaStream || !socket || !isExercising) {
        console.log('Cannot start streaming:', { 
            mediaStream: !!mediaStream, 
            socket: !!socket, 
            isExercising 
        });
        return;
    }

    console.log('🎬 Starting frame streaming...');
    canvas.width = videoWidth;
    canvas.height = videoHeight;
    
    let frameCount = 0;

    function processFrame() {
        if (socket && socket.connected && isExercising) {
            context.drawImage(videoElement, 0, 0, videoWidth, videoHeight);
            const imageData = canvas.toDataURL('image/jpeg', 0.7);
            socket.emit('frame', imageData);
            
            frameCount++;
            if (frameCount % 30 === 0) {
                console.log(`📹 Sent ${frameCount} frames`);
            }
        }

        if (isExercising && mediaStream && mediaStream.active) {
            requestAnimationFrame(processFrame);
        } else {
            console.log('🛑 Stopped streaming frames');
        }
    }

    processFrame();
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
    }
    if (socket) {
        socket.disconnect();
    }
});

console.log('✅ workout.js loaded successfully');