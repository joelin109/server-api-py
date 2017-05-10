from bs4 import BeautifulSoup, Comment
from selenium import webdriver  # 导入Selenium的webdriver
import time
from selenium.webdriver.common.keys import Keys


class HttpSeleniumCrawler:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    waiting_time = 15
    url = 'https://unsplash.com'
    frame_id = None

    def __init__(self, url=None, frame_id=None):
        if url is not None:
            self.url = url
        if frame_id is not None:
            self.frame_id = frame_id

    def start_crawl(self):
        _soup = self._crawl_source()
        # print(_soup.prettify())

        # For http://music.163.com/
        _soups = _soup.find_all('div', class_='u-cover u-cover-alb3')
        for _soup in _soups:
            _img = _soup.img
            if 'src' in _img.attrs:
                print(_img['src'])

        # For https://unsplash.com
        _soup_a = _soup.find_all('a', class_='cV68d')
        for _a in _soup_a:
            if 'style' in _a.attrs:
                _style = _a['style']
                _style_first_pos = _style.index('(') + 1
                _style_second_pos = _style.index(')')
                _a_img_src = _style[_style_first_pos: _style_second_pos]
                # print(_a_img_src)

    def _crawl_source(self):
        _driver = webdriver.PhantomJS()
        _driver.get(self.url)
        self._scroll_down(driver=_driver, times=1)  # 执行网页下拉到底部操作，执行3次
        if self.frame_id is not None:
            _driver.switch_to.frame(self.frame_id)

        return BeautifulSoup(_driver.page_source, 'lxml')

    def _scroll_down(self, driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1), "次下拉操作")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 执行JavaScript实现网页下拉倒底部
            time.sleep(self.waiting_time)  # 等待30秒，页面加载出来再执行下拉操作


def crawl_http_url(crawl_url=None):
    _url = 'http://music.163.com/#/artist/album?id=101988&limit=120&offset=0'
    _crawler = HttpSeleniumCrawler(_url, 'g_iframe')
    _crawler.start_crawl()

    print(' ---crawl_http_url ---- Done----')
