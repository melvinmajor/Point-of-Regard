import json

FRAME_RATE = 34  # 34 frames / seconde
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


data = readDataFromJsonFile(PATH_TO_JSON_FILE)


def numberOfDataPerSecond(j):
    """
    Permet de calculer la moyenne en parcourant le nombre d'itérations de la même seconde

    :param j : permet de rester à la seconde voulue
    :return :
    """
    count = 0
    # j = 0
    lengthData = len(data)
    for key in range(j, lengthData):
        k = data[key]
        time = data[j]["time"][0:3]
        if k["time"][0:3] == time:
            count += 1
        else:
            return count


def avgDataPerSecond():
    """
    :return: un fichier json avec la moyenne des données par seconde
    """
    sommeLporX = 0.0
    sommeLporY = 0.0
    sommeRporX = 0.0
    sommeRporY = 0.0
    i = 0
    j = 0
    for key in data:
        try:
            # SOMME DES DONNEES PAR SECONDE
            sommeLporX = sommeLporX + float(key['LporX'])
            sommeLporY = sommeLporY + float(key['LporY'])
            sommeRporX = sommeRporX + float(key['RporX'])
            sommeRporY = sommeRporY + float(key['RporY'])
            if len(data):
                if int(data[i]["time"][0:3]) != int(data[i + 1]["time"][0:3]):
                    print("seconde ", data[i]["time"][0:3])
                    # MOYENNE DES DONNEES
                    moyLporX = sommeLporX / numberOfDataPerSecond(j)
                    moyLporY = sommeLporY / numberOfDataPerSecond(j)
                    moyRporX = sommeRporX / numberOfDataPerSecond(j)
                    moyRporY = sommeRporY / numberOfDataPerSecond(j)
                    print(round(moyLporX, 4), '\n', round(moyLporY, 4), '\n', round(moyRporX, 4), '\n',
                          round(moyRporY, 4))
                    j = j + numberOfDataPerSecond(j) # J Permet de rester à la même seconde
                    # INITIALISATION des données pour reprendre àpd la seconde suivante
                    sommeLporX = 0.0
                    sommeLporY = 0.0
                    sommeRporX = 0.0
                    sommeRporY = 0.0
            i += 1
        except:
            pass


avgDataPerSecond()
