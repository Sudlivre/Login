
"""
# 安装tesseract-ocr
sudo apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev
tesseract  --list-langs
# 语言
git clone https://github.com/tesseract-ocr/tessdata.git
sudo mv tessdata/* /usr/share/tesseract-ocr/tessdata

# 安装库
pip3 install tesserocr pillow
"""

import tesserocr
from PIL import Image


# image = Image.open('images/code01.jpg')
# result = tesserocr.image_to_text(image)
# print(result)

# print(tesserocr.file_to_text('images/code01.jpg'))

# 转灰度
# image = Image.open('images/code01.jpg')
# image = image.convert('L')
# image.show()

# 二值化
# image.convert('1')
# image.show()

# 指定二值化的阈值，默认127
image = Image.open('images/code02.jpg')
image = image.convert('L')
threshold = 80
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')
image.show()
result = tesserocr.image_to_text(image)
print(result)