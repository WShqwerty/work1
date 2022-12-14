from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def main():
    print("work start!")
    # change page num;
    n = 20
    urls = []
    name = ""
    urls_get = []
    for i in range(1, n+1):
        # url http://www.177picyy.com/html/2022/01/4772612.html
        urls.append(f"http://www.177picyy.com/html/2022/01/4772612.html/{i}/")
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
                urls_get.append(data.get_attribute("data-lazy-src"))
        with open(f"url.txt", "w")as f:
            f.write(name+"\n")
            for url in urls_get:
                f.write(url+"\n")
            f.close()
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()