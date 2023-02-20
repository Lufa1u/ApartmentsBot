import time

from fake_useragent import UserAgent

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium_stealth import stealth


ua = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument(f'--proxy-server={proxy}')


options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(
    options=options, executable_path='X:/projects/Avito_Apartment_Parser/ChromeDriver/chromedriver.exe')


stealth(driver,
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?localPriority=0"
links = []
driver.get(url)
block = driver.find_element(By.CLASS_NAME, 'index-root-KVurS')
html = block.get_attribute('innerHTML')
soup = bs(html, 'lxml')
refs = soup.find_all(
    'a', class_='link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ title-listRedesign-_rejR title-root_maxHeight-X6PsH')
for ref in refs:
    links.append('https://www.avito.ru' + ref['href'])
print(links)
time.sleep(5)
driver.quit()
