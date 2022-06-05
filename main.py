
from pdf2image import convert_from_path
import pytesseract
import cv2
import pandas as pd
import glob
import os
folder_path = 'D:\кейс\cистема_анализа_российского_рынка_средств_измерений\Система анализа российского рынка средств измерений\тест пдф'
countrydict = {}
yeardict = {}
path = 'D:/кейс/cистема_анализа_российского_рынка_средств_измерений/Система анализа российского рынка средств измерений/тест задача 2/'
dataframe = pd.read_csv(path + '001 AoErMS0xMDA0NTE4NDA=.csv', sep=';', encoding='Windows-1251')
dataframe['страна']=''
dataframe['год_утверждения']=''
for filename in glob.glob(os.path.join(folder_path, '*.pdf')):
  pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
  images = convert_from_path(filename, 500,poppler_path=r'D:\poppler-0.68.0_x86\poppler-0.68.0\bin')
  endname=os.path.basename(filename)
  endname=os.path.splitext(endname)[0]


  for i, image in enumerate(images):
      fname = 'image'+str(i)+'.png'
      image.save(fname, "PNG")
      pages=i
  img = cv2.imread('image'+str(pages)+'.png')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
  dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
  contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  im2 = img.copy()
  country=['российская федерация','россия','абхазия','австралия','австрия','азербайджан','аргентина','армения','беларусь','бельгия',
         'болгария','бразилия','великобритания','венгрия','вьетнам','гаити','германия','голландия',
         'нидерланды','гондурас','гонконг','греция','грузия','дания','доминиканская республика',
         'египет','израиль','индия','индонезия','иордания','ирак','иран','ирландия','испания',
         'италия','казахстан','камерун','канада','кипр','киргызстан','китай','корея','коста-Рика',
         'куба','кувейт','латвия','ливан','ливия','литва','люксембург','македония','малайзия',
         'мальта','мексика','мозамбик','молдова','монако','монголия','марокко','новая зеландия',
         'о.а.э.','объединенные арабские эмираты','пакистан','перу','польша','португалия','румыния',
         'сша','соединенные штаты америки','сальвадор','сингапур','сирия','словакия','словения',
         'суринам','таджикистан','тайвань','тайланд','тунис','туркменистан','туркмения','туркс и кейкос',
         'турция','уганда','узбекистан','украина','финляндия','франция','хорватия','чехия','чили',
         'швейцария','швеция','эквадор','эстония','юар','югославия','южная корея','ямайка','япония']
  remembercountry=''
  for cnt in contours:
          x, y, w, h = cv2.boundingRect(cnt)
          # Рисуем прямоугольник на скопированном изображении
          rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
          # кроппим текстовый блок для добавления в tesseract
          cropped = im2[y:y + h, x:x + w]
          # открываем файл для записи
          file = open("recognized.txt", "a")

          # ищем текст
          text = pytesseract.image_to_string(cropped, lang='rus', config='--oem 3 --psm 4')
          text=text.lower()
          word=text.split()
          word=''.join(word)
          if word.endswith('.'):
              word = word[:-1]
          count=country.count(word)
          if count>0:
              remembercountry=word
              break
  yearkey=endname[:4]
  indexkey=endname[5:].split('.')
  yeardict.setdefault(yearkey,indexkey)
  countrydict.setdefault(remembercountry,indexkey)

dataframe['страна']=dataframe['Номер_в_госреестре'].map(countrydict)
dataframe['год_утверждения']=dataframe['Номер_в_госреестре'].map(yeardict)
print(dataframe.head(10))
dataframe.to_csv('dataframe1.csv')