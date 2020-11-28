# from bs4 import BeautifulSoup
# from selenium import webdriver
# from PIL import Image
# from io import BytesIO
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from pathlib import Path
from pytesseract import image_to_string

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bolotov\AppData\Local\Tesseract-OCR\tesseract.exe'
#
# driver = webdriver.Chrome('chromedriver.exe')
#
#
# while True:
#     driver.get('https://www.avito.ru/moskva/telefony/iphone_7_silver_2002276705')
#     if 'Доступ с Вашего IP временно ограничен' in str(driver.page_source):
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#
#         element = driver.find_element_by_xpath('/html/body/div/div/form/fieldset/div/img')
#         location = element.location
#         size = element.size
#         png = driver.get_screenshot_as_png()  # saves screenshot of entire page
#
#         im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
#
#         left = location['x']
#         top = location['y']
#         right = location['x'] + size['width']
#         bottom = location['y'] + size['height']
#
#         im = im.crop((left, top, right, bottom))  # defines crop points
#         im.save('screenshot.png')  # saves new cropped image
#
#
#         # Grayscale, Gaussian blur, Otsu's threshold
#         image = cv2.imread('screenshot.png')
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         blur = cv2.GaussianBlur(gray, (3, 3), 0)
#         thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
#         # Morph open to remove noise and invert image
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#         opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
#         invert = 255 - opening
#
#         # Perform text extraction
#         data = pytesseract.image_to_string(invert, lang='rus', config='--psm 6')
#         print(data)
#
#         cv2.imshow('thresh', thresh)
#         cv2.imshow('opening', opening)
#         cv2.imshow('invert', invert)
#         cv2.waitKey()
#
#
#         # image = cv2.imread('screenshot.png')
#         # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#         # thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#         # thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
#         #
#         # data = pytesseract.image_to_string(thresh, lang='rus', config='--psm 6')
#         # print(data)
#         input('enter')
#         # print(soup.prettify())
#


def get_white_mask(
  img,
  lower=np.array([100,100,100]),
  upper=np.array([255,255,255])):
    return cv2.inRange(img, lower, upper)


def ocr(img_url, **tess_kwargs):
    img = get_white_mask(cv2.imread(img_url))
    return image_to_string(img, **tess_kwargs)


a = ocr(img_url='screenshot.png')
print(a)