import unittest


from main import *


class TestUtils(unittest.TestCase):
    def test_checkIfFileExists(self):
        self.assertTrue(expr=checkIfFileExists("./Testbilder/1_1.jpg"))
        self.assertFalse(checkIfFileExists("./Testbilder/1.jpg"))
        with self.assertRaises(TypeError):
            checkIfFileExists()

    def test_openImage(self):
        with self.assertRaises(TypeError):
            openImage()
        filename = "./Testbilder/1_1.jpg"
        self.assertEqual(Image.open(filename), openImage(filename))

    def test_getColorToPixel(self):
        image = openImage("./Testbilder/1_1.jpg")
        with self.assertRaises(TypeError):
            getColorToPixel()

        with self.assertRaises(TypeError):
            getColorToPixel(image)

        with self.assertRaises(TypeError):
            getColorToPixel((1, 1))

        self.assertEqual((251, 245, 231), getColorToPixel(image, (0, 0)))

        with self.assertRaises(IndexError):
            getColorToPixel(image, (10000, 10000))

        with self.assertRaises(IndexError):
            getColorToPixel(image, (10000, -10000))

    def test_compareSizesOfImages(self):
        # image1 = openImage("./Testbilder/1_1.jpg")

        with self.assertRaises(TypeError):
            getColorToPixel()


unittest.main()
