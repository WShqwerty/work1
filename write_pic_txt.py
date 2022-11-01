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


def main():
    print("hello")
    urls = []
    with open("url.txt", "r")as f:
        urls = f.readlines()
        f.close()
    name = urls[0]
    urls.pop(0)
    mkdir(f"photo/{name}")
    driver1 = webdriver.Chrome()
    driver2 = webdriver.Chrome()
    driver3 = webdriver.Chrome()
    driver4 = webdriver.Chrome()
    drivers = [driver1, driver2, driver3, driver4]
    threads = []
    i = 0
    try:
        while i < len(urls):
            if os.path.exists(f'photo/{name}/{i+1}.png'):
                i += 1
                continue
            if len(drivers) > 0:
                thread = UrlThread(drivers[0], urls[i], i+1, name, drivers)
                drivers.pop(0)
                thread.start()
                threads.append(thread)
                i += 1
                percent = int(i/len(urls)*50)
                print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{i}/{len(urls)}', end=".")
        print()
    finally:
        for td in threads:
            td.join()
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
