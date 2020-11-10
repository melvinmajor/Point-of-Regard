#import cv2
import json
import time
import numpy as np
import cv2

from matplotlib import pyplot as plt, image as mpimg
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name

# variable definition
FRAME_RATE = 34
PATH_TO_VIDEO = "data/test-your-awareness.avi"
PATH_TO_JSON_FILE = "PoR-data.json"


def readDataFromJsonFile(path):
    """
    permet de lire les données venant d'un fichier JSON

    :param path: chemin vers le fichier à lire
    :return: un tableau d'objets JSON (iteratif)
    """
    with open(path) as json_file:
        return json.load(json_file)


def simpleConcatData(data, frameCount):
    """
    TODO : implémenter la partie du code faisant la moyenne des différents paquets

    Permet de séparer les datas passées en paramètre en petits paquets. Le nombre de data par paquet
    est déterminé par la taille des datas et le nombre de frames de la vidéo

    :param data: tableau d'objets à trier
    :param frameCount: le nombre de d'images d'une vidéo
    :return: un tableau d'objets JSON (iteratif)(TODO)
    """
    dataNumber = len(data)
    length = frameCount
    packetSize = round(dataNumber / length)
    cutFrequency = round(dataNumber / (packetSize * length - dataNumber))

    frameIncr = 0
    packetIncr = 0

    return_data = []

    for index, p in enumerate(data):

        packetIncr += 1

        if packetIncr == 1:
            return_data[frameIncr] = p

        else:

            if (index+1) % cutFrequency == 0:

                    packetIncr += 1

            if packetIncr >= packetSize:

                    packetIncr = 0
                    frameIncr += 1

    print("total" + str(frameIncr))


data = readDataFromJsonFile(PATH_TO_JSON_FILE)

cap = cv2.VideoCapture(PATH_TO_VIDEO)

fig, ax = plt.subplots()

img = mpimg.imread('moi.jpg')

imgplot = plt.imshow(img)


#simpleConcatData(data, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

# Check if camera opened successfully


### Cette partie du code permet de lire la video avec CV2 ##############################

"""if (cap.isOpened() == False):
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
cv2.destroyAllWindows()"""