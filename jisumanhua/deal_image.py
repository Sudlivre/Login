import math
import operator
import os
from functools import reduce

from PIL import Image

from config import GROUP_END

IMAGE_NAME = 1


def cut_image(image_name):
    global IMAGE_NAME
    image = Image.open('./full_images/' + str(image_name) + '.jpg')
    im1 = image.crop((0, 0, 76, 76))
    im1.save('./single_images/' + str(IMAGE_NAME) + '.jpg')
    IMAGE_NAME += 1
    im2 = image.crop((76, 0, 152, 76))
    im2.save('./single_images/' + str(IMAGE_NAME) + '.jpg')
    IMAGE_NAME += 1
    im3 = image.crop((152, 0, 228, 76))
    im3.save('./single_images/' + str(IMAGE_NAME) + '.jpg')
    IMAGE_NAME += 1
    im4 = image.crop((228, 0, 304, 76))
    im4.save('./single_images/' + str(IMAGE_NAME) + '.jpg')
    IMAGE_NAME += 1


def deal_image():
    image_name = [str(i) for i in range(1, GROUP_END * 4 + 1)]
    i = 0
    while i < len(image_name) - 1:
        print(f'正在处理第{i+1}张图片')
        img1 = './single_images/' + image_name[i] + '.jpg'
        j = i + 1
        while j < len(image_name):
            img2 = './single_images/' + image_name[j] + '.jpg'
            # print(f'正在对比第{image_name[i]},{image_name[j]}两张图片')
            result = image_contrast(img1, img2)
            # print('对比结果：', result)
            if result < 10:
                image_name.remove(image_name[j])
                print('删除图片：', img2)
                os.remove(img2)
            j += 1
        i += 1


def image_contrast(img1, img2):
    image1 = Image.open(img1)
    image2 = Image.open(img2)
    h1 = image1.histogram()
    h2 = image2.histogram()
    result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return result


def main():
    for i in range(1, GROUP_END + 1):
        print(f'正在裁剪第{i}张图片')
        cut_image(i)
    deal_image()


if __name__ == '__main__':
    main()
