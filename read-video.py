#!/usr/bin/python3 -u
# coding=utf8
import json

import cv2
from plot import readVideo

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
    """
        Permet de faire la moyenne de la donnée passée en paramètre. Le format attendu pour la donnée est :
        {sumX: <la_somme_des_x>, sumY:<la_somme_des_y>}
        :param data: la donnée dont on voudrait moyenner les coordonnées
        :return: les données moyennées le format {x: <moyenne_en_x>, y:<moyenne_en_y>}
    """
    if (not data["validate"]):
        tempX = data["sumX"] / 20
        tempY = data["sumY"] / 20
    else:
        tempX = data["sumX"] / 19
        tempY = data["sumY"] / 19
    moyenne = {"x": tempX, "y": tempY}

    return moyenne


def simpleConcatData(data, frameCount):
    """
        Permet de séparer les datas passées en paramètre en petits paquets. Le nombre de data par paquet
        est déterminé par la taille des datas et le nombre de frames de la vidéo
        :param data: tableau d'objets à trier
        :param frameCount: le nombre de d'images d'une vidéo
        :return: un tableau d'objets JSON (iteratif)
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
            if (index + 1) % cutFrequency == 0:
                isCut = True
                packetIncr += 1

            if packetIncr >= packetSize:
                moyenne = moyenneData({'sumX': sumX, 'sumY': sumY, 'validate': isCut})
                return_data[frameIncr]["LporX"] = moyenne["x"]
                return_data[frameIncr]["LporY"] = moyenne["y"]

                packetIncr = 0
                frameIncr += 1

                sumX = 0.0
                sumY = 0.0
                isCut = False

    return return_data


def fuseData(xArray, yArray):
    """
        permet de fusionner deux tableaux de coordonnées x et y.

        :param xArray: tableau des coordonnées x des points
        :param yArray: tableau des coordonnées y des points
        :return: un tableau d'objet contenant les coordonnées x et y des points
    """
    returnArray = []

    for index, elem in enumerate(xArray):
        returnArray.append({'LporX': elem, 'LporY': yArray[index]})

    return returnArray


def getTimeFromJsonFile(data):
    """
        permet de réccupérer tous les temps des données passées en paramètre

        :param data: tableau de données JSON
        :return: un tableau contenant les temps.
    """
    time = []

    for index, p in enumerate(data):
        if index == len(data) - 1:
            pass
        else:
            time.append(int(p["time"]) - int(data[0]["time"]))

    return time


def getXFromJsonFile(data):
    """
        permet de réccupérer toutes les coordonnées x des données passées en paramètre

        :param data: tableau de données JSON
        :return: un tableau contenant les coordonnées x.
    """
    x = []

    for p in data:
        try:
            x.append(float(p["LporX"]))
        except KeyError:
            continue

    return x


def getYFromJsonFile(data):
    """
        permet de réccupérer toutes les coordonnées y des données passées en paramètre

        :param data: tableau de données JSON
        :return: un tableau contenant les coordonnées y.
    """
    y = []

    for p in data:
        try:
            y.append(float(p["LporY"]))
        except KeyError:
            continue

    return y


data = readDataFromJsonFile(PATH_TO_JSON_FILE)

cap = cv2.VideoCapture(PATH_TO_VIDEO)

superData = simpleConcatData(data, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

tabX = getXFromJsonFile(superData)
tabY = getYFromJsonFile(superData)

filterX = savgol_filter(tabX, 11, 1)
filterY = savgol_filter(tabY, 11 , 1)

tabTimes = getTimeFromJsonFile(data)

s = int(tabTimes[len(tabTimes) - 1])

timePerImage = np.linspace(0, s, 1708)

spl1 = UnivariateSpline(timePerImage, filterX, k=5)
spl2 = UnivariateSpline(timePerImage, filterY, k=5)

xArray = spl1(timePerImage)
yArray = spl2(timePerImage)

newData = fuseData(xArray, yArray)

readVideo(newData)
