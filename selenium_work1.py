from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import solution as sl


def main():
    print("start working!")
    value = input("please input what you want search:")
    url = f"https://www.xvideos.com/?k={value}"
    driver = webdriver.Chrome()
    result = []
    try:
        driver.get(url)
        sleep(5)
        datas = driver.find_elements(By.XPATH, '//div[@class="thumb-under"]/p/a')
        for data in datas:
            result.append([data.get_attribute("title"), data.get_attribute("href")])
    finally:
        driver.close()
        driver.quit()
    sl.write_to_csv(result, ["title", "href"], "excelfile/result/xvideo.csv")

if __name__ == "__main__":
    main()
