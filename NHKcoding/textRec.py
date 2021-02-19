from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from pytesseract import pytesseract
import cv2

filePath = 'data/a.png'
# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# image = Image.open(filePath)
# image.load()
# # print(pytesseract.image_to_string(image, lang='jpn'))

# # pytesseract.run_tesseract(filePath, 'output', lang='jpn', config="hocr")

# boxes = pytesseract.image_to_data(image, lang="jpn")

# image = cv2.imread(filePath)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# gray2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# gray3 = cv2.medianBlur(gray, 3)

# cv2.imwrite('out3.png', gray3)

# im = Image.open(filePath)
# im = im.filter(ImageFilter.MedianFilter())
# enhancer = ImageEnhance.Contrast(im)
# im = enhancer.enhance(2)
# im = im.convert('1')
# im.save('out4.png')

LEVEL_INDEX = 0
LEFT_INDEX = 6
TOP_INDEX = 7
WIDTH_INDEX = 8
HEIGHT_INDEX = 9
TEXT_INDEX = 11


text_out = ''
k = 0

tempName = '2.png'
sourceImage = Image.open(tempName)
text0 = pytesseract.image_to_data(sourceImage, lang='jpn')

w, h, x = cv2.imread(tempName).shape

textBoxes = text0.split('\n')
for line in textBoxes:
	words = line.split('\t')
	if words[0] == '5':
		print(words[TEXT_INDEX])
		left = int(words[LEFT_INDEX])
		right = int(words[WIDTH_INDEX]) + left
		top = int(words[TOP_INDEX])
		bottom = int(words[HEIGHT_INDEX]) + top
		draw = ImageDraw.Draw(sourceImage)
		draw.rectangle([left, top, right, bottom], fill=None, outline='orange')


# for oneBox in textBoxes:
# 	box = oneBox.split(' ')
# 	left = int(box[1])
# 	bottom = w-int(box[2])
# 	right = int(box[3])
# 	top = w-int(box[4])
	
# 	draw = ImageDraw.Draw(sourceImage)

# 	print([left, top, right, bottom])
# 	draw.rectangle([left, top, right, bottom], fill=None, outline='orange')
# sourceImage.show()


