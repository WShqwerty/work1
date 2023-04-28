from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def main():
    print("hello world!")
    # urls_o = "https://krhentai.com/chapter_54877.html"
    # urls_o = "https://krhentai.com/chapter_54878.html"
    # urls_o = "https://krhentai.com/chapter_54879.html"
    # urls_o = "https://krhentai.com/chapter_54880.html"
    # urls_o = "https://krhentai.com/chapter_54881.html"
    urls_o = "https://krhentai.com/chapter_54882.html"
    driver = webdriver.Chrome()
    urls = []

    try:
        driver.get(urls_o)
        sleep(2)
        photos = driver.find_elements(By.XPATH, '//li[@class="comic-page"]/img')
        for photo in photos:
            urls.append(photo.get_attribute("src"))
    finally:
        driver.close()
        driver.quit()

    if len(urls) != 1:
        with open(f"url.txt", "a")as f:
            for url in urls:
                f.write(url+"\n")
            f.close()


if __name__ == "__main__":
    main()