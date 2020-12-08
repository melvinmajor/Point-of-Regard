import matplotlib.pyplot as plt
import cv2
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from scipy.interpolate import interp1d, UnivariateSpline

PATH_TO_VIDEO = "data/test-your-awareness.avi"
FRAME_RATE = 30
FRAME_HIGH = 710
FRAME_LENGTH = 950

""" ******************************** fonctions de testing  ********************************* """


def funnyDot(dot):
    dot['positive_x'] = positivitySwitch(dot['x'], dot['positive_x'], FRAME_LENGTH)
    dot['positive_y'] = positivitySwitch(dot['y'], dot['positive_y'], FRAME_HIGH)

    moveXDot(dot)
    moveYDot(dot)

    return dot


def moveXDot(dot):
    if dot['positive_x']:
        dot['x'] += 5

    else:
        dot['x'] -= 5


def moveYDot(dot):
    if dot['positive_y']:
        dot['y'] += 5

    else:
        dot['y'] -= 5


def positivitySwitch(dotCoordinate, dotPositivity, limit):
    if dotCoordinate >= limit or dotCoordinate <= 0:
        return not dotPositivity
    else:
        return dotPositivity


""" ********************************* Fonctions principales ********************************** """


def windowRenderer():
    fig, ax = plt.subplots(figsize=(12, 9))
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)

    ax.axis('off')

    return fig, ax


def plotDotOnImage(image, dot):
    fig, ax = windowRenderer()

    canvas = FigureCanvas(fig)

    ax.imshow(image)

    # PLOTTING : plot the dot to the x, y position
    ax.plot(dot['x'], dot['y'], 'bo')

    canvas.draw()
    buf = canvas.buffer_rgba()
    # convert to a NumPy array
    X = np.asarray(buf)

    # Remove this for test the matplotlib plot

    # plt.show()

    cv2.imshow('frame', X)


def readVideo(data):

    cap = cv2.VideoCapture(PATH_TO_VIDEO)

    movingDot = {'x': 0, 'y': 0, 'positive_x': False, 'positive_y': False}

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    i = 0

    # Read until video is completed
    while (cap.isOpened()):

        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        movingDot = {'x': data[i]["LporX"]/1.6, 'y': data[i]["LporY"]/1.6, 'positive_x': False, 'positive_y': False}

        # cv2.waitKey(int(1000/FRAME_RATE))
        plotDotOnImage(frame, movingDot)

        #funnyDot(movingDot)
        ##################  Permet de transformer en image le plot  #######################################

        plt.close('all')

        if cv2.waitKey(1) == ord('q'):
            break
    
        i+=1

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


def customReadVideo(data):
    cap = cv2.VideoCapture(PATH_TO_VIDEO)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    i = 0

    # Read until video is completed
    while (cap.isOpened()):

        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        movingDot = {'x': data[i]["LporX"] / 1.6, 'y': data[i]["LporY"] / 1.6, 'positive_x': False, 'positive_y': False}

        cv2.waitKey(int(1000/FRAME_RATE))

        drawSquarre(30, int(data[i]["LporX"] / 1.6), int(data[i]["LporY"] / 1.6), frame)

        cv2.imshow('frame', frame)

        plt.close('all')

        if cv2.waitKey(1) == ord('q'):
            break

        i += 1

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


""" *********************************** TODO functions ****************************************** """

"""def drawCircle(radius, x_center, y_center, list, image, color):

    x=0,
    y=radius
    m=5-4*radius

    while x <=y :
        list[x_center+x][y_center+y] = "*"
        list[x_center+y][y_center+x] = "*"
        list[x_center-x][y_center+y] = "*"
        list[x_center-y][y_center+x] = "*"
        list[x_center+x][y_center+y] = "*"
        list[x_center+y][y_center+x] = "*"
        list[x_center-x][y_center-y] = "*"
        list[x_center-y][y_center-x] = "*"

        if m > 0 :
            y -= 1
            m = m+8*x+4



    print (list)
"""

def drawSquarre(size, y_center, x_center, image, color=[0, 255, 0]):

    if(size > 0):
        image[x_center][y_center] = color

    for x in range(-size+1, size):
        for y in range(-size+1, size):

            image[x_center + x][y_center + y]=color

def drawMap(min_x, max_x, min_y, max_y, image, color=[0, 255, 0]):

    for x in range(min_x, max_x):

        for y in range (min_y, max_y):

            image[x][y] = color


""" ***************************** for modifying pixel ******************************** """

"""for i in range(100):
    for y in range(100):
        frame[i][y] = [0, 0, 255]     point = {'x':500, 'y':500}
 """
