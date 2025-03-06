const videoElement = document.getElementById('video');
const startButton = document.getElementById('startExercise');
const stopButton = document.getElementById('EndExercise');
const status = document.getElementById('status')

let mediaStream = null;
let websocket = null;
let videoWidth = 640;
let videoHeight = 480;


const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

startButton.addEventListener('click', async () => {
    try {

        mediaStream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: videoWidth },
                height: { ideal: videoHeight }
            } 
        });

        videoElement.srcObject = mediaStream;

        socket = io('http://localhost:5000');

        socket.on('connect', () => {
            console.log('Socket.IO connection established');
            startStreamingFrames();
        });

        socket.on('error', (error) => {
            console.error('Socket.IO Error:', error);
        });

        socket.on('disconnect', () => {
            console.log('Socket.IO connection closed');
        });

        socket.on('response', (data) => {
            console.log('Server response:', data.message);
        });
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Could not access camera. Please check permissions.');
    }
});

function startStreamingFrames() {
    if (!mediaStream || !socket) return;

    canvas.width = videoWidth;
    canvas.height = videoHeight;

    function processFrame() {
        if (socket.connected) {

            context.drawImage(videoElement, 0, 0, videoWidth, videoHeight);

            const imageData = canvas.toDataURL('image/jpeg', 0.7);

            socket.emit('frame', imageData);
        }

        if (mediaStream.active) {
            requestAnimationFrame(processFrame);
        }
    }

    processFrame();
}

stopButton.addEventListener('click', () => {
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
    }

    if (socket) {
        socket.disconnect();
    }
});