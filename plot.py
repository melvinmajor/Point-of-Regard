import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cv2
import numpy as np

PATH_TO_VIDEO = "data/test-your-awareness.avi"
FRAME_RATE = 1000
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

    # TODO : Optimize this part because it's cause fps drop
    canvas.draw()
    buf = canvas.buffer_rgba()
    # convert to a NumPy array
    X = np.asarray(buf)

    # Remove this for test the matplotlib plot

    # plt.show()

    cv2.imshow('frame', X)


def readVideo(x, y):

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

        movingDot = {'x': x[i]/1.6, 'y': y[i]/1.6, 'positive_x': False, 'positive_y': False}

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


""" *********************************** TODO functions ****************************************** """

"""def drawCircle(radius, x_center, y_center, image, color):

    squarre_radius = (radius-1)*(radius-1)
    list = []

    for i in range((2*radius)+1):

        stock = []
        for j in range((2*radius)+1):
            stock.append("o")
        list.append(stock)

    for i in (0, radius):

        x = 0
        i_squarre = i * i
        while (squarre_radius - i_squarre >= x * x):
            list[radius + x][radius + i] = "*"
            list[radius + x][radius - i] = "*"
            list[radius + i][radius - x] = "*"
            list[radius - i][radius - x] = "*"
            x+=1


    for i in list :
        string = ""
        for y in i:
            string+=y

        print(string)


drawCircle(2, 0, 0, "test", "test")"""

""" ***************************** for modifying pixel ******************************** """

"""for i in range(100):
    for y in range(100):
        frame[i][y] = [0, 0, 255]     point = {'x':500, 'y':500}
 """
