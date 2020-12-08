import json

import cv2
from plot import readVideo, customReadVideo

from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter

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

def fuseData(xArray, yArray):

    returnArray=[]

    for index, elem in enumerate(xArray):

        returnArray.append({'LporX': elem, 'LporY': yArray[index]})

    return returnArray

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

def getDynamicMap(rawData, middleData, frameCount):
    dataNumber = len(rawData)
    length = frameCount
    packetSize = round(dataNumber / length)
    cutFrequency = round(dataNumber / (packetSize * length - dataNumber))

    frameIncr = 0
    packetIncr = 0

    sumX = 0.0
    sumY = 0.0
    isCut = False
    return_data = []

    for index, p in enumerate(rawData):

        packetIncr += 1
        try:
            sumX += float(p["LporX"])
            sumY += float(p["LporY"])
        except KeyError:
            continue

        if (index + 1) % cutFrequency == 0:
            isCut = True
            packetIncr += 1

        if packetIncr >= packetSize:
            moyenne = moyenneData({'sumX': sumX, 'sumY': sumY, 'validate': isCut})
            return_data.append({'x_center': rawData[frameIncr]["LporX"], 'y_center': rawData[frameIncr]["LporX"], })
            return_data[frameIncr]["LporX"] = moyenne["x"]
            return_data[frameIncr]["LporY"] = moyenne["y"]

            packetIncr = 0
            frameIncr += 1

            sumX = 0.0
            sumY = 0.0
            isCut = False

    return return_data


def getMapDatas(rawData, distance, x_center, y_center):

    min_x, max_x, min_y, max_y = getWindowRange(rawData)

    map=[]

    i = 1

    while max_x - i*distance > x_center and max_y - i*distance > y_center:

        range= []

        for elem in rawData:

            if inRange(int(elem["LporX"]), int(elem["LporY"]), distance, min_x, max_x, min_y, max_y):

                range.append(elem)


def inRange(x, y, distance, min_x, max_x, min_y, max_y):

    if (x < min_x+distance and x >= min_x) or (x <= max_x and x > max_x-distance):

        if (y >= min_y and y < min_y+distance) or (y <= max_y and y > max_y-distance):

            return True
        else:
            return False

    if (y >= min_y and y < min_y + distance) or (y <= max_y and y > max_y - distance):

        if (x < min_x + distance and x >= min_x) or (x <= max_x and x > max_x - distance):

            return True
        else:
            return False

    return False

def getWindowRange(rawData):

    min_x= 1000
    min_y= 1000
    max_x= 0
    max_y= 0

    for elem in rawData:

        if int(elem["LporX"]) < min_x:
            min_x =  int(elem["LporX"])

        if int(elem["LporX"]) > max_x:
            min_x =  int(elem["LporX"])

        if int(elem["LporY"]) < min_y:
            min_x =  int(elem["LporX"])

        if int(elem["LporY"]) > max_y:
            min_x =  int(elem["LporX"])

    return min_x, max_x, min_y, max_y

data = readDataFromJsonFile(PATH_TO_JSON_FILE)

cap = cv2.VideoCapture(PATH_TO_VIDEO)

superData = simpleConcatData(data, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

tabX = getXFromJsonFile(superData)
tabY = getYFromJsonFile(superData)


filterX = savgol_filter(tabX, 11, 1)
filterY = savgol_filter(tabY, 11, 1)

tabTimes = getTimeFromJsonFile(data)

s = int(tabTimes[len(tabTimes)-1])

timePerImage = np.linspace(0, s, 1708)

spl1 = UnivariateSpline(timePerImage, filterX, k=5)
spl2 = UnivariateSpline(timePerImage, filterY, k=5)

xArray = spl1(timePerImage)
yArray = spl2(timePerImage)

newData = fuseData(xArray, yArray)

customReadVideo(newData)
