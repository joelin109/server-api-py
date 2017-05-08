from selenium import webdriver  # 导入Selenium的webdriver
from selenium.webdriver.common.keys import Keys


def crawl_http_url(crawl_url=None):
    _driver = webdriver.Chrome()
    print(_driver)
