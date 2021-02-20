import cv2
import os
from pytesseract import image_to_string
from PIL import Image

ABSOLUTE_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'

def main():
  imagePath = os.path.join(ABSOLUTE_FILE_PATH, 'img/img1.jpg')
  rgbImage = Image.open(imagePath)
  print(image_to_string(rgbImage, lang='eng'))


if __name__ == "__main__":
  main()
