from bs4 import BeautifulSoup as bs

from fake_useragent import UserAgent

import requests
from requests.exceptions import ConnectionError, ProxyError, ReadTimeout, SSLError

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from selenium_stealth import stealth


class MyProxy:

    list_ip = []

    def __init__(self):
        MyProxy.list_ip = self.get_proxy()

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    def get_list_ip(self, html):
        soup = bs(html, "lxml")
        elements = soup.find("tbody").find_all("tr")
        for element in elements:
            ip = element.find_all("td")[0].text
            port = element.find_all("td")[1].text
            proxy = "{}:{}".format(ip, port)
            self.list_ip.append(proxy)
        return self.list_ip

    def get_proxy(self):
        url = "https://www.sslproxies.org/"
        html = self.get_html(url)
        list_ip = self.get_list_ip(html)
        return list_ip


my_proxy = MyProxy()


def create_driver(proxy: str = None):
    if proxy is None:
        proxy = MyProxy.list_ip[-1]

    ua = UserAgent()

    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    options.add_argument("headless")
    options.add_argument("ignore-certificate-errors")
    options.add_argument("ignore-certificate-errors-spki-list")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--proxy-server={proxy}")

    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
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
        'a', class_='link-link-MbQDP link-design-default-_nSbv title-root-zZCwT iva-item-title-py3i_ ' +
                    'title-listRedesign-_rejR title-root_maxHeight-X6PsH')
    for ref in refs:
        links.append('https://www.avito.ru' + ref['href'])
    return links


def search_apart(url):
    driver = create_driver()
    list_ip = my_proxy.list_ip
    for ip in list_ip:
        try:
            driver.get(url)
            html = driver.find_element(
                By.CLASS_NAME, 'index-root-KVurS').get_attribute('innerHTML')
            result = soup_parser(html)
            if result != '':
                driver.quit()
                return result
            else:
                continue
        except (ProxyError, ConnectionError, ReadTimeout, SSLError, WebDriverException):
            driver = create_driver(ip)
            list_ip.pop(list_ip.index(ip))
            continue


def check():
    url = 'https://hidemy.name/ru/what-is-my-ip/'
    errors = 0
    ips = []
    driver = create_driver()
    list_ip = my_proxy.list_ip
    for ip in list_ip:
        try:
            driver.get(url)
            html = driver.find_element(By.CLASS_NAME, 'ip')
            soup = bs(html.text, 'lxml')
            my_ip = str(soup)
            print(my_ip)
            ips.append(my_ip)
        except (ProxyError, ConnectionError, ReadTimeout, SSLError, WebDriverException):
            driver = create_driver(ip)
            list_ip.pop(list_ip.index(ip))
            errors = errors + 1
            continue
    driver.quit()
    print(ips)
    print(errors)
