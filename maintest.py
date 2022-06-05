from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import pytesseract
from numpy import asarray
import cv2
images = convert_from_path("D:/кейс/cистема_анализа_российского_рынка_средств_измерений/Система анализа российского рынка средств измерений/Дата-сет для задачи №1/Разметка/2005-30815-05.pdf", 500,poppler_path=r'D:\poppler-0.68.0_x86\poppler-0.68.0\bin')
for i, image in enumerate(images):
    fname = 'image'+str(i)+'.png'
    image.save(fname, "PNG")
    pages=i

low_green = np.array([31, 225, 72])
high_green = np.array([131, 255, 255])
def greentext(imagename):
 while True:
    img = cv2.imread(imagename)
    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgHSV = cv2.bilateralFilter(imgHSV, 11, 17, 17)
    # create the Mask
    mask = cv2.inRange(imgHSV, low_green, high_green)
    res = cv2.bitwise_and(img, img, mask=mask)
    break
 return res


imgreen = Image.fromarray(greentext('image1.png'))

imgreen.save("greencut.PNG")

img = Image.open('cutcut.PNG')
thresh = 10
fn = lambda x : 255 if x > thresh else 0
r = imgreen.convert('L').point(fn, mode='1')
r.save('greencut.PNG')

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
def ocr_core(filename):
  """ This function will handle the core OCR processing of images. """
  text = pytesseract.image_to_string(Image.open(filename),config='-l rus --oem 3 --psm 7 -c tessedit_char_blacklist=0123456789')
  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
  return text
def ocr_core_number(filename):
  """ This function will handle the core OCR processing of images. """
  text = pytesseract.image_to_string(Image.open(filename),config='-l rus --oem 3 --psm 12 -c tessedit_char_whitelist=0123456789,./+-')
  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
  return text
def ocr_core1(filename):
  """ This function will handle the core OCR processing of images. """
  text = pytesseract.image_to_string(Image.open(filename),config='-l rus --oem 3 --psm 7')
  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
  return text

#numbers=ocr_core_number('greencut.PNG')
#print('Текст: ', text)
#print('Погрешность: ', numbers)
text=ocr_core1('greencut.PNG')
print(text)