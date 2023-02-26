from bs4 import BeautifulSoup as bs

from fake_useragent import UserAgent

import asyncio

import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium_stealth import stealth


class MyProxy:

    good_list_ip = []
    ip = ''

    def __init__(self) -> None:
        self.get_proxy()

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    def get_list_ip(self, html):
        list_ip = []
        soup = bs(html, "lxml")
        elements = soup.find("tbody").find_all("tr")
        for element in elements:
            ip = element.find_all("td")[0].text
            port = element.find_all("td")[1].text
            proxy = "{}:{}".format(ip, port)
            list_ip.append(proxy)
        return list_ip

    def get_proxy(self):
        url = "https://www.sslproxies.org/"
        html = self.get_html(url)
        list_ip = self.get_list_ip(html)
        for ip in list_ip:
            try:
                r = requests.get("https://yandex.ru/", proxies={"https": "http://" + ip}, timeout=1)
                if r.status_code == 200:
                    MyProxy.good_list_ip.append(ip)
            except Exception:
                continue
        print(f'Настройка завершена, добавлено {len(MyProxy.good_list_ip)} прокси')


my_proxy = MyProxy()


def create_driver():
    if my_proxy.good_list_ip == []:
        my_proxy.get_proxy()
    elif my_proxy.ip == '':
        my_proxy.ip = my_proxy.good_list_ip[0]
        my_proxy.good_list_ip.pop(0)

    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    options.add_argument("headless")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("ignore-certificate-errors-spki-list")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--proxy-server={my_proxy.ip}")

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(
        options=options, executable_path='X:/projects/Avito_Apartment_Parser/ChromeDriver/chromedriver.exe')

    stealth(driver,
            user_agent=str(ua.ff),
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


def soup_parser(html):
    links = []
    soup = bs(html, 'lxml')
    refs = soup.find_all(
        'a', class_='link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ ' + 'title-listRedesign-_rejR title-root_maxHeight-X6PsH')
    if refs is not None:
        for ref in refs:
            links.append('https://www.avito.ru' + ref['href'])
        return links


def search_apart(url) -> str:
    while True:
        try:
            driver = create_driver()
            driver.get(url)
            html = driver.find_element(
                By.CLASS_NAME, 'index-root-KVurS').get_attribute('innerHTML')
            links = soup_parser(html)
            driver.quit()
            return links[0]
        except Exception:
            my_proxy.ip = ''
            driver.quit()
            continue
