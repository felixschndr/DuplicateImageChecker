#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PIL import Image
from os.path import exists, getsize, basename
from argparse import ArgumentParser
from os import cpu_count
from itertools import combinations
from glob import glob
import sys
from joblib import Parallel, delayed
from time import time


STEP_SIZE = 100
ALLOWED_DEVIATION = 80


def convert_seconds_to_minutes_and_seconds(elapsedSeconds):
    minutes = (elapsedSeconds // 60) % 60
    seconds = elapsedSeconds % 60

    return int(minutes), int(seconds)


def open_image(imagePath):
    return Image.open(imagePath)


def get_color_to_pixel_of_image(image, pixel):
    return image.getpixel(pixel)


def compare_image_sizes(image1, image2):
    # Prüfen, ob die Größen der Bilder vielfache voneinander sind
    skaling_faktor = image1.width / image2.width
    if image1.height == image2.height * skaling_faktor:
        return skaling_faktor

    return 0


def compare_colors_of_images(image1, image2, skaling_faktor):
    for x in range(0, image1.width, STEP_SIZE):  # Vergleich auf x
        for y in range(0, image1.height, STEP_SIZE):  # Vergleich auf y
            image1R, image1G, image1B = get_color_to_pixel_of_image(image1, (x, y))
            image2R, image2G, image2B = get_color_to_pixel_of_image(image2, (x / skaling_faktor, y / skaling_faktor))

            red_in_deviation = image1R - ALLOWED_DEVIATION <= image2R <= image1R + ALLOWED_DEVIATION
            green_in_deviation = image1G - ALLOWED_DEVIATION <= image2G <= image1G + ALLOWED_DEVIATION
            blue_in_deviation = image1B - ALLOWED_DEVIATION <= image2B <= image1B + ALLOWED_DEVIATION

            if not (red_in_deviation and green_in_deviation and blue_in_deviation):
                return False

    return True


def print_duplicate_images(bild1, bild2):
    image1DiskSpace = getsize(bild1)
    image2DiskSpace = getsize(bild2)

    print(f" - {basename(bild1)} ({image1DiskSpace / 1000}KB) und {basename(bild2)} ({image2DiskSpace / 1000}KB)")
    print(f'       rm "{bild1 if image2DiskSpace > image1DiskSpace else bild2}"')


def compare_images(image1Path, image2Path):
    image1 = open_image(image1Path)
    image2 = open_image(image2Path)

    skaling_faktor = compare_image_sizes(image1, image2)
    if skaling_faktor == 0:
        # Bildergrößen sind keine Vielfachen von einander
        return False
    elif skaling_faktor == 1:
        # Genau die gleiche Bildergröße somit handelt es sich nicht um das gleiche Bild, wenn die Dateigrößen unterschiedlich sind
        if getsize(image1Path) != getsize(image2Path):
            return False

    if compare_colors_of_images(image1, image2, skaling_faktor):
        print_duplicate_images(image1Path, image2Path)


def startComparissonForPath(path):  # main method
    all_files = glob(path.replace("\\", "/") + "/*.jp*g")
    number_of_combinations = sum(1 for _ in combinations(all_files, 2))

    if number_of_combinations == 0:
        print("Es wurden keine Bilder im genannten Verzeichnis gefunden!")
        sys.exit(1)

    print(f"Überprüfe {len(all_files)} Bilder mit {number_of_combinations} Kombinationen")

    global_start_time = time()
    Parallel(n_jobs=(cpu_count() - 1))(
        delayed(compare_images)(combination[0], combination[1]) for combination in combinations(all_files, 2)
    )
    global_end_time = time()

    minutes, seconds = convert_seconds_to_minutes_and_seconds(global_end_time - global_start_time)
    print(f"--> Fertig nach {minutes} Minuten und {seconds} Sekunden")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", help="Pfad, der geprüft werden soll", required=False)
    args = parser.parse_args()

    path = args.path if args.path else input("Pfad, der geprüft werden soll: ")

    if not exists(path):
        print(f'\nDas Verzeichnis "{path}" existiert nicht!')
        sys.exit(1)

    startComparissonForPath(path)
