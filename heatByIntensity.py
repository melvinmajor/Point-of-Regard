import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL.Image import *

# ---------------------------
def heatByIntensity():
    i = open("Result.jpg")
    new_I = open("Result2.jpg")
    (rouge, vert, bleu) = (0, 0, 0)
    jaune = (255, 222, 0)
    orange = (255, 145, 0)
    red = (255, 68, 0)
    (larg, haut) = i.size
    for x in range(larg):
        for y in range(haut):
            (rouge, vert, bleu) = i.getpixel((x, y))
            if rouge <= 90 and vert <= 90:
                new_I.putpixel((x, y), jaune)
            if rouge <= 70 and vert <= 70:
                new_I.putpixel((x, y), orange)
            if rouge <= 40 and vert <= 40:
                new_I.putpixel((x, y), red)
    Image.show(new_I)


heatByIntensity()

# ---------------------------