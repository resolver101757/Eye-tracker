# opens the camera and displays the feed to test openCV can access the camera

import cv2

# Initialize the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Camera could not be opened.")
else:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame is read correctly
        if not ret:
            print("Error: Can't receive frame. Exiting...")
            break
        
        flipped_frame = cv2.flip(frame, 0)
        
        # Display the resulting frame
        cv2.imshow('Camera Feed', flipped_frame)

        # Break the loop with 'q' key
        if cv2.waitKey(1) == ord('q'):
            break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
