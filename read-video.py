import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name

# number of images per second
FRAME_RATE = 34


cap = cv2.VideoCapture("data/test-your-awareness.avi")

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened()):

    ret, frame = cap.read()

# if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.waitKey(int(1000/FRAME_RATE))
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()