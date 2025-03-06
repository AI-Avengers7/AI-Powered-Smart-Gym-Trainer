import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)  # 0 is the default camera

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("Failed to capture frame")
        break

    # Display the frame in a window
    cv2.imshow('Webcam Feed', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()