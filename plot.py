import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cv2
import numpy as np
import time

PATH_TO_VIDEO = "data/test-your-awareness.avi"
FRAME_RATE = 1000
FRAME_HIGH = 710
FRAME_LENGTH = 950

def funnyDot(dot):

    dot['positive_x'] = positivitySwitch(dot['x'], dot['positive_x'], FRAME_LENGTH)
    dot['positive_y'] = positivitySwitch(dot['y'], dot['positive_y'], FRAME_HIGH)

    moveXDot(dot)
    moveYDot(dot)

    return dot


def moveXDot(dot) :

    if dot['positive_x']:
        dot['x'] += 5

    else :
        dot['x'] -= 5


def moveYDot(dot) :

    if dot['positive_y']:
        dot['y'] += 5

    else:
        dot['y'] -= 5


def positivitySwitch(dotCoordinate, dotPositivity, limit):

    if dotCoordinate >= limit or dotCoordinate <= 0 :
        return not dotPositivity
    else :
        return dotPositivity

def plotDotOnImage(image, dot) :

    fig, ax = plt.subplots(figsize=(12, 9))
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)

    canvas = FigureCanvas(fig)

    ax.axis('off')
    ax.imshow(image)

    # PLOTTING : plot the dot to the x, y position
    ax.plot(dot['x'], dot['y'], 'bo')

    # imgplot = plt.imshow(image)

    #TODO : Optimize this part because it's cause fps drop
    canvas.draw()
    buf = canvas.buffer_rgba()
    # convert to a NumPy array
    X = np.asarray(buf)

    #Remove this for test the matplotlib plot
    #plt.show()

    cv2.imshow('frame', X)


cap = cv2.VideoCapture(PATH_TO_VIDEO)

movingDot = {'x': 0, 'y': 0, 'positive_x' : False, 'positive_y' : False }

if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Read until video is completed
while (cap.isOpened()):

    ret, frame = cap.read()

# if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #cv2.waitKey(int(1000/FRAME_RATE))

    #point = {'x':500, 'y':500}
    plotDotOnImage(frame, movingDot)

    funnyDot(movingDot)
##################  Permet de transformer en image le plot  #######################################

    plt.close('all')

    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

