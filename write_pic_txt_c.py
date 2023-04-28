import os
import threading
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


class UrlThread(threading.Thread):
    def __init__(self, id, name, urls):
        threading.Thread.__init__(self)
        self.name = name
        self.id = id
        self.urls = urls

    def run(self):
        write_pic(self.name, self.id, self.urls)


def write_pic(name, id, urls):
    driver = webdriver.Chrome()
    try:
        for url in urls:
            driver.get(url)
            sleep(1)
            element = driver.find_element(By.XPATH, "//img")
            element.screenshot(f'photo/{name}/{id}.png')
            id += 1
    finally:
        driver.close()
        driver.quit()


def main():
    print("hello")
    urls = []
    with open("url.txt", "r")as f:
        urls = f.readlines()
        f.close()
    name = urls[0]
    urls.pop(0)
    mkdir(f"photo/{name}")

    urls_four = int(len(urls)/4)
    if len(urls)%4 != 0:
        urls_four += 1
    
    url_one = urls[0:urls_four:]
    url_two = urls[urls_four:urls_four*2:]
    url_three = urls[urls_four*2:urls_four*3:]
    url_four = urls[urls_four*3:len(urls):]

    threads = []
    url_thread1 = UrlThread(1, name, url_one)
    url_thread1.start()
    threads.append(url_thread1)
    url_thread2 = UrlThread(urls_four+1, name, url_two)
    url_thread2.start()
    threads.append(url_thread2)
    url_thread3 = UrlThread(urls_four*2+1, name, url_three)
    url_thread3.start()
    threads.append(url_thread3)
    url_thread4 = UrlThread(urls_four*3+1, name, url_four)
    url_thread4.start()
    threads.append(url_thread4)

    for td in threads:
        td.join()


if __name__ == "__main__":
    main()

