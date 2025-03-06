const videoElement = document.getElementById('video');
const startButton = document.getElementById('startExercise');
const stopButton = document.getElementById('EndExercise');

let mediaStream = null;
let websocket = null;
let videoWidth = 640;
let videoHeight = 480;


// Create canvas for frame processing
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

startButton.addEventListener('click', async () => {
  try {
      // Request camera access
      mediaStream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
              width: { ideal: videoWidth },
              height: { ideal: videoHeight }
          } 
      });
      
      // Set video source to camera stream
      videoElement.srcObject = mediaStream;

      // Setup WebSocket connection
      websocket = new WebSocket('ws://localhost:5000/ws');

      websocket.onopen = () => {
          console.log('WebSocket connection established');
          startStreamingFrames();
      };

      websocket.onerror = (error) => {
          console.error('WebSocket Error:', error);
      };

      websocket.onclose = () => {
          console.log('WebSocket connection closed');
      };
  } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Could not access camera. Please check permissions.');
  }
});

function startStreamingFrames() {
  if (!mediaStream || !websocket) return;

  canvas.width = videoWidth;
  canvas.height = videoHeight;

  function processFrame() {
      if (websocket.readyState === WebSocket.OPEN) {
          // Draw current video frame to canvas
          context.drawImage(videoElement, 0, 0, videoWidth, videoHeight);
          
          // Convert canvas to base64
          const imageData = canvas.toDataURL('image/jpeg', 0.7);
          
          // Send frame via WebSocket
          websocket.send(imageData);
      }

      // Continue streaming if camera is active
      if (mediaStream.active) {
          requestAnimationFrame(processFrame);
      }
  }

  // Start frame processing
  processFrame();
}

stopButton.addEventListener('click', () => {
  if (mediaStream) {
      // Stop all tracks
      mediaStream.getTracks().forEach(track => track.stop());
      videoElement.srcObject = null;
  }

  if (websocket) {
      websocket.close();
  }
});