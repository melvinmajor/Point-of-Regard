import os
import json
import logging
import logging.handlers

FRAME_RATE = 34  # 34 frames / seconde
PATH_TO_VIDEO = "data/test-your-awareness.avi"
PATH_TO_JSON_FILE = "PoR-data.json"
TMP_FILE = "tmp-average.txt"
FINAL_JSON_FILE = "PoR-data-average.json"


''' Log configuration '''
logger = logging.getLogger('avgCalculate')
logger.setLevel(logging.INFO)
LOG_ROTATE = 'midnight'
# create a file handler and timed rotating
handler = logging.handlers.TimedRotatingFileHandler('avgCalculate.log', when=LOG_ROTATE, backupCount=7, utc=False) # 7 days backup
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
alice = logging.StreamHandler()
alice.setFormatter(formatter)
logger.addHandler(alice)


# Fail method
def fail(msg):
    print(">>> Oops:",msg,file=sys.stderr)
    logger.warning('Oops: %s', msg)


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


def toJson(seconde, LporX, LporY, RporX, RporY):
    """
    :param seconde: corresponding second
    :param LporX: point of regard position, left eye, x direction, in pixels
    :param LporY: point of regard position, left eye, y direction, in pixels
    :param RporX: point of regard position, right eye, x direction, in pixels
    :param RporY: point of regard position, right eye, y direction, in pixels
    :return: formatted value in JSON
    """
    bob = {
        'time': seconde,
        'LporX': LporX,
        'LporY': LporY,
        'RporX': RporX,
        'RporY': RporY
    }
    return bob


def tempWriteJson(bobLikesToBeATemporaryFile):
    try:
        with open(TMP_FILE, 'a') as f:
            f.writelines(bobLikesToBeATemporaryFile)
            f.close()
            logger.info('Data written in temporary file successful')
    except IOError as e:
        fail('IOError while trying to open and write temporary file')


def writeJson():
    """
    :return: Nothing as this function is used to write data directly in JSON
    """
    #bobIsDumping = json.dumps(bobIsWaiting, indent = 2)
    #bobIsSwitching = bobIsDumping
    logger.info('Source file path: %s', FINAL_JSON_FILE)
    bobIsWaiting = []
    try:
        with open(TMP_FILE, 'r') as f:
            for line in f:
                value = list(line.strip().split())
                logger.debug(value)
                # Creating dictionary for each parameter
                temp_data = {
                    'time': value[0],
                    'LporX': value[1],
                    'LporY': value[2],
                    'RporX': value[3],
                    'RporY': value[4]
                }
                bobIsWaiting.append(temp_data)
    except IOError as e:
        fail('IOError while trying to open and read source file')
        raise

    try:
        # Creating the JSON file
        with open (FINAL_JSON_FILE, 'w') as f:
            json.dump(bobIsWaiting, f, indent=2)
        f.close()
        os.remove('tmp-average.txt')  # Delete temporary file as not useful anymore
        logger.info('Data written in JSON file successful')
    except IOError as e:
        fail('IOError while trying to open and write JSON file')


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
                    seconde = data[i]["time"][0:3]
                    logger.info('Working on second : %s', seconde)
                    # MOYENNE DES DONNEES
                    logger.debug('Making average of Point-of-Regard data')
                    ''' Moyenne somme valeurs divisé par nbre valeurs dans somme (max 4 valeurs après virgule) '''
                    moyLporX = round((sommeLporX / numberOfDataPerSecond(j)), 4)
                    moyLporY = round((sommeLporY / numberOfDataPerSecond(j)), 4)
                    moyRporX = round((sommeRporX / numberOfDataPerSecond(j)), 4)
                    moyRporY = round((sommeRporY / numberOfDataPerSecond(j)), 4)
                    logger.debug('Converting data to JSON format...')
                    dataToTmp = (str(seconde), ' ', str(moyLporX), ' ', str(moyLporY), ' ', str(moyRporX), ' ',
                                 str(moyRporY), '\n')
                    tempWriteJson(dataToTmp)
                    writeJson()
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
