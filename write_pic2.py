import threading
from time import sleep
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from photo import test


class UrlThread(threading.Thread):
    def __init__(self, driver, url, id, name, drivers):
        threading.Thread.__init__(self)
        self.driver = driver
        self.url = url
        self.drivers = drivers
        self.id = id
        self.name = name

    
    def run(self):
        write_pic(self.driver, self.url, self.name, self.id)
        self.drivers.append(self.driver)


def write_pic(driver, path, name, id):
    sleep(1)
    driver.get(path)
    sleep(1)
    element = driver.find_element(By.XPATH, "//img")
    element.screenshot(f'photo/{name}/{id}.png')


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def get_name(url):
    driver = webdriver.Chrome()
    name = ''
    try:
        driver.get(url)
        sleep(1)
        name = driver.find_element(By.XPATH, '//div[@class="col-md-8"]/h3/span[@class="pretty"]').text
        mkdir(f"photo/{name}")
    finally:
        driver.close()
        driver.quit()
    return name


def get_num(url):
    driver = webdriver.Chrome()
    num = ''
    try:
        driver.get(url+"/1")
        sleep(1)
        url_photo = driver.find_element(By.XPATH, '//div[@id="comic-content-wrapper"]/img').get_attribute('src')
        num = url_photo.split('/')[4]
        print(num)
    finally:
        driver.close()
        driver.quit()
    return num


def main():
    print("work start!")

    n = 206
    m = 80035

    url_page = "https://hanime1.me/comic/"+str(m)

    name = get_name(url_page)
    num = get_num(url_page)

    urls = ["https://i.nhentai.net/galleries/"+num+"/"+str(i)+".jpg" for i in range(1, n+1)]
    driver1 = webdriver.Chrome()
    driver2 = webdriver.Chrome()
    driver3 = webdriver.Chrome()
    driver4 = webdriver.Chrome()
    drivers = [driver1, driver2, driver3, driver4]
    threads = []
    len_urls = len(urls)
    i = 1
    try:
        while i-1 < len(urls):
            if os.path.exists(f'photo/{name}/{i+1}.png'):
                i += 1
                continue
            if len(drivers) > 2:
                thread = UrlThread(drivers[0], urls[i], i, name, drivers)
                drivers.pop(0)
                thread.start()
                threads.append(thread)
                i += 1
                percent = int(i/len_urls*50)
                print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{i}/{len_urls}', end=".")
        print()
    finally:
        driver1.close()
        driver1.quit()
        driver2.close()
        driver2.quit()
        driver3.close()
        driver3.quit()
        driver4.close()
        driver4.quit()


if __name__ == "__main__":
    main()
    # test.work_test('Nyotaika Heaven | 女體化天國', "https://i.nhentai.net/galleries/2340829/2.jpg", "1")