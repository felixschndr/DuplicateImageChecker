# DuplicateImageChecker

- Prints all duplicate images in a given directory by checking their color pixel values in a grid.
- Also recognizes images that are not the same exact size if their dimensions are mutiples from each other
- Prints all duplicate images and their sizes so you can decide which copy to keep.

## Usecase
I use this tool to remove any duplicate images I got sent from other people in whatsapp.

## Example
```
$ python main.py

Prüfe 21 Kombinationen im Ordner ./Testbilder
 - 1_1.jpg (186.171KB) und 1_2.jpg (186.171KB)
 - 3_high.jpg (207.322KB) und 3_low.jpg (207.322KB)
 - 4_original.jpg (6331.378KB) und 4_whatsapp.jpg (167.172KB)
```
- `1_1.jpg` and `1_2.jpg` are the same image
- `3_high.jpg` and `3_low.jpg` are the same image (both chewup up by whatsapp)
- `4_original.jpg` and `4_whatsapp.jpg` are the same image but only `4_whatsapp.jpg` was compressed by whatsapp