import threading
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import solution as sl
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


def main():
    print("work start!")
    datas = sl.read_from_csv("photo/urls/177.csv")
    name = datas[0][0]
    mkdir(f'photo/{name}')
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver1 = webdriver.Chrome(chrome_options=option)
    driver2 = webdriver.Chrome(chrome_options=option)
    driver3 = webdriver.Chrome(chrome_options=option)
    driver4 = webdriver.Chrome(chrome_options=option)
    drivers = [driver1, driver2, driver3, driver4]
    threads = []
    i = 0
    try:
        while i < len(datas):
            if os.path.exists(f'photo/{name}/{i+1}.png'):
                i += 1
                continue
            if len(drivers) > 0:
                thread = UrlThread(drivers[0], datas[i][1], i+1, name, drivers)
                drivers.pop(0)
                thread.start()
                threads.append(thread)
                i += 1
                percent = int(i/len(datas)*50)
                print(f'\r[{"#"*percent}{"."*(50-percent)}]\t{i}/{len(datas)}', end=".")
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
    # test.work_test('[中文][甲斐ひろゆき] 僕の山ノ上村孕ませ日記 (我的山中農村配種日記)[225P]', "http://img.177picyy.com/uploads/2015/08b/2256.jpg", "224")
