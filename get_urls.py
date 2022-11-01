from selenium import webdriver
from selenium.webdriver.common.by import By
import solution as sl
from time import sleep


def main():
    print("work start!")
    n = 14
    urls = []
    urls_get = []
    for i in range(1, n+1):
        urls.append(f"http://www.177picyy.com/html/2014/02/39635.html/{i}/")
    driver = webdriver.Chrome()
    try:
        i = 0
        for url in urls:
            driver.get(url)
            sleep(1)
            name = driver.find_element(By.XPATH, '//header[@class="entry-header"]/h1').text
            datas = driver.find_elements(By.XPATH, '//div[@class="single-content"]/p/img')
            for data in datas:
                i += 1
                urls_get.append([name, data.get_attribute("data-lazy-src")])
        sl.write_to_csv(urls_get, ["id", "url"], "photo/urls/177.csv")
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()