import cv2
import os
import pytesseract
from pytesseract import image_to_string
from pytesseract import Output
from google_trans_new import google_translator

ABSOLUTE_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
translator = google_translator()


def translate(word, language):
  return translator.translate(word, lang_src='en', lang_tgt=language)


def video(device, language):
  cap = cv2.VideoCapture(device)
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


def find_text(image, language, show=False):
  full_text = pytesseract.image_to_string(image)
  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
  # loop over each of the individual text localizations
  for i in range(0, len(results["text"])):
    x, y = results["left"][i], results["top"][i]
    w, h = results["width"][i], results["height"][i]
    text = results["text"][i]
    conf = int(results["conf"][i])
    if conf > 75 and len(full_text) > 3:
      text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
      text = translate(text, language)
      text = text if type(text) == str else text[0]
      cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)
      cv2.putText(image, text, (x, y+h//2), cv2.FONT_ITALIC, .4, (255, 0, 0), 1)  

  if show:
    cv2.imshow('Translated Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  return image

if __name__ == "__main__":
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('-l', action='store', default='en', type='string', dest='language', help='es, ru')
  parser.add_option('-i', action='store', default='no', type='string', dest='image', help='yes or no')
  parser.add_option('-p', action='store', default='d:/dev/cam-to-text-translator/src/img/img1.jpg', type='string', dest='image_path', help='image absolute path')
  parser.add_option('-v', action='store', default='no', type='string', dest='video', help='yes or no')
  parser.add_option('-d', action='store', default='http://192.168.1.17:4747/mjpegfeed?640x480', type='string', dest='device', help='video device, 0 for laptop camera or ip address for ip camera')

  (options, args) = parser.parse_args()

  if options.image == 'yes':
    find_text(cv2.imread(options.image_path), options.language, show=True)
  
  if options.video == 'yes':
    if options.device.isdigit(): options.device = int(options.device)
    video(options.device, options.language)
