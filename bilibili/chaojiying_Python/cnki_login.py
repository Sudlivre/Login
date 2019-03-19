import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
from chaojiying_Python.chaojiying import check_code

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)


def cnki_login():
    url = 'http://login.cnki.net/login/'
    browser.get(url)
    email = wait.until(EC.presence_of_element_located((By.ID, 'TextBoxUserName')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'TextBoxPwd')))
    email.send_keys(EMAIL)
    time.sleep(1)
    password.send_keys(PASSWORD)
    time.sleep(1)
    try:
        check_code_input = wait.until(EC.presence_of_element_located((By.ID, 'CheckCode')))
    except TimeoutException:
        pass
    else:
        captcha = check_code_image()
        json_data = check_code(captcha)
        check_code_input.send_keys(json_data['pic_str'])

    login_btn = wait.until(EC.presence_of_element_located((By.ID, 'Button1')))
    login_btn.click()


def get_screenshot():
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def get_position():
    img = wait.until(EC.presence_of_element_located((By.ID, 'CheckCodeImg')))
    time.sleep(2)
    location = img.location
    size = img.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']
    return (top, bottom, left, right)


def check_code_image(name='captcha.png'):
    top, bottom, left, right = get_position()
    print('验证码位置', top, bottom, left, right)
    screenshot = get_screenshot()
    captcha = screenshot.crop((left, top, right, bottom))
    captcha.save(name)
    return captcha


def main():
    cnki_login()


if __name__ == '__main__':
    main()
