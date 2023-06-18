import cv2
import numpy as np

# First we load the pre-trained cascade file which detect our face
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Take the mask image which you want to augment over your face with transparent background
mask = cv2.imread('mask.jpg', cv2.IMREAD_UNCHANGED)

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()

    # Convert the webcam frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # run a loop over detected faces
    for (x, y, w, h) in faces:
        # resize the mask
        resized_mask = cv2.resize(mask, (w, h))

        mask_alpha = resized_mask[:, :, 3] / 255.0

        mask_inverse = 1.0 - mask_alpha

        mask_bgr = resized_mask[:, :, :3]

        # Adjust the mask position to match the face
        x_offset = x
        y_offset = y
        x_end = x + w
        y_end = y + h

        for c in range(3):
            frame[y_offset:y_end, x_offset:x_end, c] = (
                mask_alpha * mask_bgr[:, :, c] +
                mask_inverse * frame[y_offset:y_end, x_offset:x_end, c]
            )

    # Display the frame
    cv2.imshow('AR Face Mask', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
