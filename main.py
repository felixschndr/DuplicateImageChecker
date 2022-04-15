#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from os.path import exists, getsize, basename, dirname
from os import cpu_count
from itertools import combinations
from glob import glob
from sys import exit
from joblib import Parallel, delayed
from time import time


UNTERORDNER_PRUEFEN = False  # max-depth = 1
SCHRITT_GROESSE = 100
ABWEICHUNG = 80


def time_convert(elapsedSeconds):
    minutes = (elapsedSeconds // 60) % 60
    seconds = elapsedSeconds % 60
    print("--> Fertig nach {} Minuten und {} Sekunden".format(int(minutes), int(seconds)))


def checkIfFileExists(inputPath):
    fileExists = exists(inputPath)
    if not fileExists:
        print('Die Datei "' + str(inputPath) + '" existiert nicht!')
    return fileExists


def openImage(imagePath):
    return Image.open(imagePath)


def getColorToPixel(image, pixel):
    return image.getpixel(pixel)


def compareSizesOfImages(image1, image2):
    # Prüfen, ob die Größen der Bilder vielfache voneinander sind
    skaling_faktor = image1.width / image2.width
    if image1.height == image2.height * skaling_faktor:
        return skaling_faktor

    return 0


def compareColorsOfImages(image1, image2, skaling_faktor):
    for x in range(0, image1.width, SCHRITT_GROESSE):  # Vergleich auf x
        for y in range(0, image1.height, SCHRITT_GROESSE):  # Vergleich auf y
            image1R, image1G, image1B = getColorToPixel(image1, (x, y))
            image2R, image2G, image2B = getColorToPixel(image2, (x / skaling_faktor, y / skaling_faktor))
            rotInAbweichung = image1R - ABWEICHUNG <= image2R <= image1R + ABWEICHUNG
            gruenInAbweichung = image1G - ABWEICHUNG <= image2G <= image1G + ABWEICHUNG
            blauInAbweichung = image1B - ABWEICHUNG <= image2B <= image1B + ABWEICHUNG
            if not (rotInAbweichung and gruenInAbweichung and blauInAbweichung):
                return False

    return True


def printDuplicateImages(bild1, bild2):
    image1DiskSpace = getsize(bild1)
    image2DiskSpace = getsize(bild2)
    print(
        (" - {} ({}KB) und {} ({}KB)").format(
            basename(bild1), image1DiskSpace / 1000, basename(bild2), image2DiskSpace / 1000
        )
    )
    print(('       rm "{}"\n').format(bild1 if image2DiskSpace > image1DiskSpace else bild2))


def compareImages(image1Path, image2Path):
    # print(f'\r{round(counter/anzahlKombinationen*100, 2)} %', end="")
    # print("Vergleiche Bild {} mit {}".format(
    #     basename(image1Path), basename(image2Path)))
    image1 = openImage(image1Path)
    image2 = openImage(image2Path)
    if not (checkIfFileExists(image1Path) and checkIfFileExists(image2Path)):
        return False

    skaling_faktor = compareSizesOfImages(image1, image2)
    if skaling_faktor == 0:
        return False

    sameImage = compareColorsOfImages(image1, image2, skaling_faktor)
    if sameImage:
        printDuplicateImages(image1Path, image2Path)


def startComparissonForPath(PFAD):
    alleDateien = glob(PFAD.replace("\\", "/") + "*.jp*g")
    anzahlKombinationen = sum(1 for _ in combinations(alleDateien, 2))

    if anzahlKombinationen == 0:
        print("Es wurden keine Bilder im genannten Verzeichnis gefunden!")
        exit(1)

    print("Überprüfe {} Bilder mit {} Kombinationen".format(len(alleDateien), anzahlKombinationen))

    startTime = time()

    Parallel(n_jobs=cpu_count())(
        delayed(compareImages)(kombination[0], kombination[1]) for kombination in combinations(alleDateien, 2)
    )

    endTime = time()
    time_convert(endTime - startTime)


def getAllDirectionsInPath(Pfad):
    alleOrdner = glob(Pfad + "/*/", recursive=False) if UNTERORDNER_PRUEFEN else glob(Pfad + "/", recursive=False)

    for ordner in alleOrdner:
        startComparissonForPath(ordner)


if __name__ == "__main__":
    path = input("Pfad, der geprüft werden soll: ")
    if not exists(path):
        print('\nDas Verzeichnis "' + str(path) + '" existiert nicht!')
        exit(1)

    getAllDirectionsInPath(path)
