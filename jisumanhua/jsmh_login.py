import os
import random
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JiSuManHuaLogin(object):

    def __init__(self, email, password):
        self.url = 'http://www.1kkk.com/'
        self.email = email
        self.password = password
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.window_size = self.browser.set_window_size(1300, 600)

    def get_code(self):
        """
        获取图片验证码列表
        :return:
        """
        self.browser.get(self.url)
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'header_login')))
        button.click()
        img_list = []
        for i in range(2, 6):
            im = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.account-login-form .form-wrap > div > div:nth-child(' + str(i) + ')')))
            img_list.append(im)
        return img_list

    def get_input(self):
        """
        输入账号密码
        :return:
        """
        email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                'body > section.modal-wrap > div > div > div > div > p:nth-child(2) > input[type="text"]')))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                   'body > section.modal-wrap > div > div > div > div > p:nth-child(3) > input[type="password"]')))
        email.send_keys(self.email)
        time.sleep(2.4)
        password.send_keys(self.password)

    def get_position(self, screen_shot, img, image_name):
        """
        从网页截图中扣出验证码图片
        :param screen_shot:
        :param img:
        :param image_name:
        :return:
        """
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        image = screen_shot.crop((left, top, right, bottom))
        image.save(image_name)
        return image

    def get_screen_shot(self):
        """
        网页截图
        :return:
        """
        time.sleep(3)
        screen_shot = self.browser.get_screenshot_as_png()
        screen_shot = Image.open(BytesIO(screen_shot))
        return screen_shot

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断图片是否相同
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def for_images_list(self, image1, images_list):
        """
        将验证码图片与图库中的图片做对比
        :param image1:
        :param images_list:
        :return:
        """
        flag = True
        for j in images_list:
            image2 = Image.open('./single_images/' + j)
            count = 0
            for _ in range(100):
                x = random.randint(10, 66)
                y = random.randint(10, 66)
                # print('测试像素：', x, y)
                result = self.is_pixel_equal(image1, image2, x, y)
                if not result:
                    flag = False
                    break
                count += 1
                if count >= 95:
                    flag = True
            if flag:
                print('成功匹配', j)
                return flag
        return flag

    def compared_image(self, i):
        """
        识别验证码，匹配不上旋转验证码
        :param i:
        :return:
        """
        image1 = Image.open(str(i) + '.png')
        images_list = os.listdir('./single_images')

        xz = 0
        for _ in range(4):
            if self.for_images_list(image1, images_list):
                return xz
            image1 = image1.rotate(270)
            xz += 1
        return None

    def run(self):
        # 弹出登录框，获取四张验证码列表
        img_list = self.get_code()
        # 输入账号密码
        iogin_info = self.get_input()
        # 获取网页截图
        screen_shot = self.get_screen_shot()
        #　抠图保存四张验证码图片
        for i in range(len(img_list)):
            self.get_position(screen_shot, img_list[i], str(i + 1) + '.png')
        # 识别图片
        count_list = []
        for i in range(1, 5):
            print('正在识别图片', i)
            count = self.compared_image(i)
            count_list.append(count)
        print(count_list)
        if None in count_list:
            print('图片识别错误，重启方法')
            return self.run()
        # 匹配成功，依次点击选装验证码
        for i in range(4):
            for _ in range(count_list[i]):
                img_list[i].click()
                time.sleep(1.4)
        # 点击登录按钮
        login = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin')))
        login.click()


def main():
    login = JiSuManHuaLogin('email', 'password')
    login.run()
    time.sleep(2)


if __name__ == '__main__':
    main()
