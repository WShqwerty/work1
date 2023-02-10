from selenium import webdriver
from selenium.webdriver.common.by import By
import solution as sl
from time import sleep


def main():
    print("work start!")
    n = 18
    urls = []
    urls_get = []
    for i in range(1, n+1):
        urls.append(f"http://www.177pica.com/html/2015/05/54519.html/{i}/")
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=option)
    try:
        i = 0
        for url in urls:
            print(f"worked! url{i}")
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