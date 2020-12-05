import json

FRAME_RATE = 34  # 34 frames / seconde
PATH_TO_VIDEO = "data/test-your-awareness.avi"
PATH_TO_JSON_FILE = "PoR-data-copy.json"


def readDataFromJsonFile(path):
    """
    permet de lire les données venant d'un fichier JSON

    :param path: chemin vers le fichier à lire
    :return: un tableau d'objets JSON (iteratif)
    """
    with open(path) as json_file:
        return json.load(json_file)


data = readDataFromJsonFile(PATH_TO_JSON_FILE)


def numberOfDataPerSecond(i):
    i -= 1
    count = 0
    time = data[i]["time"][0:3]
    for key in data:
        if key["time"][0:3] == time:
            count = count + 1
        else:
            return count  # total (160 pour la première donnée)
    print('nombre de données dans la ' + str(i) + 'è seconde : ', count)


def avgDataPerSecond():
    somme = 0
    i = 0
    j = 0
    for key in data:
        time = data[j]["time"][0:3]
        if key["time"][0:3] == time:
            # somme
            somme = somme + int(key["time"])
            print(key)
            print("i : ", i)
            i += 1
        else:
            print("leur moyenne : ", somme / numberOfDataPerSecond(i))
            j = i
            somme = 0


avgDataPerSecond()

# time = int(time) + 1
# str(time)
# 285
# 285
# 286
# 353
# ensuite faire la moyenne des points à la place du temps
