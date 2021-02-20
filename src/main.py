import cv2
import os
import pytesseract
from pytesseract import image_to_string
from pytesseract import Output
from PIL import Image, ImageDraw
from google_trans_new import google_translator
from greek_alphabet import greek_alphabet

ABSOLUTE_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
translator = google_translator()


def translate(word, language):
  return translator.translate(word, lang_src='en', lang_tgt=language)


def video(language):
  cap = cv2.VideoCapture('http://192.168.1.17:4747/mjpegfeed?640x480')
  skip, count = 100, 0
  while cap.isOpened():
    ret, image = cap.read()
    count += 1
    if ret:
      
      if count%skip == 0:
        image = find_text(image, language)
      
      cv2.imshow('frame', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cap.release()


def find_text(image, language):
  full_text = pytesseract.image_to_string(image)
  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
  # loop over each of the individual text localizations
  for i in range(0, len(results["text"])):
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]
    text = results["text"][i]
    conf = int(results["conf"][i])
    if conf > 75 and len(full_text) > 3:
      text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
      text = translate(text, language)
      text = text if type(text) == str else text[0]
      cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)
      cv2.putText(image, text, (x, y+10), cv2.FONT_ITALIC, .4, (255, 0, 0), 1)  

  return image

if __name__ == "__main__":
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--language', action='store', default='en', type='string', dest='language', help='es, ru')
  (options, args) = parser.parse_args()
  video(options.language)
