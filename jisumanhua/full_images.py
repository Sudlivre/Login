import requests
from multiprocessing.pool import Pool
# 定义爬取图片张数
from config import GROUP_END


def get_full_image():
    url = 'http://www.1kkk.com//image3.ashx'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except requests.exceptions.ConnectionError:
        get_full_image()


def save_to_file(data, image_name):
    with open('./full_images/' + str(image_name) + '.jpg', 'wb') as f:
        f.write(data)


def main(i):
    data = get_full_image()
    print(f'正在保存{i}张图片')
    save_to_file(data, i)


if __name__ == '__main__':
    pool = Pool()
    groups = ([i for i in range(1, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
