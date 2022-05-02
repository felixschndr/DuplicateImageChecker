#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from os.path import exists, getsize, basename
from os import cpu_count
from itertools import combinations
from glob import glob
from sys import exit
from joblib import Parallel, delayed
from time import time


STEP_SIZE = 100
ALLOWED_DEVIATION = 80


def convert_seconds_to_minutes_and_seconds(elapsedSeconds):
    minutes = (elapsedSeconds // 60) % 60
    seconds = elapsedSeconds % 60

    return int(minutes), int(seconds)


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
    for x in range(0, image1.width, STEP_SIZE):  # Vergleich auf x
        for y in range(0, image1.height, STEP_SIZE):  # Vergleich auf y
            image1R, image1G, image1B = getColorToPixel(image1, (x, y))
            image2R, image2G, image2B = getColorToPixel(image2, (x / skaling_faktor, y / skaling_faktor))

            red_in_deviation = image1R - ALLOWED_DEVIATION <= image2R <= image1R + ALLOWED_DEVIATION
            green_in_deviation = image1G - ALLOWED_DEVIATION <= image2G <= image1G + ALLOWED_DEVIATION
            blue_in_deviation = image1B - ALLOWED_DEVIATION <= image2B <= image1B + ALLOWED_DEVIATION

            if not (red_in_deviation and green_in_deviation and blue_in_deviation):
                return False

    return True


def printDuplicateImages(bild1, bild2):
    image1DiskSpace = getsize(bild1)
    image2DiskSpace = getsize(bild2)

    print(f" - {basename(bild1)} ({image1DiskSpace / 1000}KB) und {basename(bild2)} ({image2DiskSpace / 1000}KB)")
    print(f'       rm "{bild1 if image2DiskSpace > image1DiskSpace else bild2}"')


def compareImages(image1Path, image2Path):
    image1 = openImage(image1Path)
    image2 = openImage(image2Path)

    skaling_faktor = compareSizesOfImages(image1, image2)
    if skaling_faktor == 0:
        # Bildergrößen sind keine Vielfachen von einander
        return False
    elif skaling_faktor == 1:
        # Genau die gleiche Bildergröße somit handelt es sich nicht um das gleiche Bild, wenn die Dateigrößen unterschiedlich sind
        if getsize(image1Path) != getsize(image2Path):
            return False

    if compareColorsOfImages(image1, image2, skaling_faktor):
        printDuplicateImages(image1Path, image2Path)


def startComparissonForPath(path):
    print(path.replace("\\", "/"))
    all_files = glob(path.replace("\\", "/") + "/*.jp*g")
    number_of_combinations = sum(1 for _ in combinations(all_files, 2))

    if number_of_combinations == 0:
        print("Es wurden keine Bilder im genannten Verzeichnis gefunden!")
        exit(1)

    print("Überprüfe {} Bilder mit {} Kombinationen".format(len(all_files), number_of_combinations))

    # startTime = time()

    global_start_time = time()

    Parallel(n_jobs=(cpu_count() - 1))(
        delayed(compareImages)(combination[0], combination[1]) for combination in combinations(all_files, 2)
    )

    global_end_time = time()
    minutes, seconds = convert_seconds_to_minutes_and_seconds(global_end_time - global_start_time)
    print(f"--> Fertig nach {minutes} Minuten und {seconds} Sekunden")


if __name__ == "__main__":
    path = input("Pfad, der geprüft werden soll: ")
    if not exists(path):
        print('\nDas Verzeichnis "' + str(path) + '" existiert nicht!')
        exit(1)

    startComparissonForPath(path)
