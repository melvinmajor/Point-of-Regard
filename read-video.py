import json

import cv2
from plot import readVideo

from scipy.interpolate import UnivariateSpline

import numpy as np


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


def moyenneData(data):
    
    if(not data["validate"]):
        tempX = data["sumX"]/20
        tempY = data["sumY"]/20
    else:
        tempX = data["sumX"]/19
        tempY = data["sumY"]/19
    moyenne = {"x": tempX,"y": tempY}

    return moyenne


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

    sumX = 0.0
    sumY = 0.0
    isCut = False
    return_data = []

    for index, p in enumerate(data):
        
        packetIncr += 1
        try:
            sumX += float(p["LporX"])
            sumY += float(p["LporY"])
        except KeyError:
            continue
        if packetIncr == 1:
            return_data.append(p)

        else:
            if (index+1) % cutFrequency == 0:

                isCut = True
                packetIncr += 1

            if packetIncr >= packetSize:

                moyenne = moyenneData({'sumX':sumX, 'sumY': sumY, 'validate': isCut})
                return_data[frameIncr]["LporX"] = moyenne["x"]
                return_data[frameIncr]["LporY"] = moyenne["y"]

                packetIncr = 0
                frameIncr += 1

                sumX = 0.0
                sumY = 0.0
                isCut = False

    return return_data


def getTimeFromJsonFile(data):

    time = []

    for index, p in enumerate(data):
        if index==len(data)-1:
            pass
        else:
            time.append(int(p["time"])-int(data[0]["time"]))

    return time


def getXFromJsonFile(data):
    x = []

    for p in data:
        try:
            x.append(float(p["LporX"]))
        except KeyError:
            continue

    return x


def getYFromJsonFile(data):
    y = []

    for p in data:
        try:
            y.append(float(p["LporY"]))
        except KeyError:
            continue

    return y


data = readDataFromJsonFile(PATH_TO_JSON_FILE)

spl1 = UnivariateSpline(getTimeFromJsonFile(data), getXFromJsonFile(data))
spl2 = UnivariateSpline(getTimeFromJsonFile(data), getYFromJsonFile(data))

s = int(data[len(data)-2]["time"])

cap = cv2.VideoCapture(PATH_TO_VIDEO)

#superData = simpleConcatData(data, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

#readVideo(superData)
