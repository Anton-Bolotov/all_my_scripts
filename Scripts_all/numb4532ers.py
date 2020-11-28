try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\bolotov\AppData\Local\Tesseract-OCR\tesseract.exe'
# image = Image.open('Screenshot_1.png')
# text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
# need_number = text.split('\n')
# print(need_number)
# if '-' in need_number:
#     result = int(need_number.split('-')[0]) - int(need_number.split('-')[1])
#     print(result)
# Load image, grayscale, Otsu's threshold

image = cv2.imread('Screenshot_1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Blur and perform text extraction
thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6 tessedit_char_whitelist=0123456789+-')
need_data = data.split('\n')[0]
# if '-' in need_data:
#     result = int(need_data.split('-')[0]) - int(need_data.split('-')[1])
#     print(result)
# else:
#     result = int(need_data.split('-')[0]) + int(need_data.split('-')[1])
#     print(result)
print(need_data)
cv2.imshow('thresh', thresh)
cv2.waitKey()