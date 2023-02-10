from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def work_test(name, url, n):
    driver = webdriver.Chrome()
    # print(url.split("/")[4])
    try:
        driver.get(url)
        sleep(1)
        element = driver.find_element(By.XPATH, '//img')
        element.screenshot("photo/"+name+"/"+n+".png")
    finally:
        driver.close()
        driver.quit()

def main():
    print('hello!')


if __name__ == "__main__":
    main()
