class HttpURlParse:
    url = ''
    html_parse_body_tag = ''
    will_del_h5_tags = ['script', 'figcaption', 'aside', 'video']
    will_del_div_tags = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']

    def __init__(self, url):
        self.url = url
        self._start_parse()

    def _start_parse(self):
        _base_url = self.url

        _article_content_pool = ['mashable.com', 'www.tagesspiegel.de']
        _del_div_tag_pool2 = ['bonus-video-card', 'newsletter-signup']
        for _url_tag in _article_content_pool:
            if _base_url.find(_url_tag) > 0:
                self.html_parse_body_tag = 'article-content'
                self.will_del_div_tags = _del_div_tag_pool2

        # www.wired.de
        if _base_url.find('www.wired.de') > 0:
            self.html_parse_body_tag = 'article-content'

        # ars - technica
        if _base_url.find('arstechnica.com') > 0:
            self.html_parse_body_tag = 'article-content post-page'

        # buzzfeed ?
        if _base_url.find('www.buzzfeed.com') > 0:
            self.html_parse_body_tag = ''

        # cnn
        if _base_url.find('www.cnn.com') > 0:
            self.html_parse_body_tag = 'zn-body__paragraph'

        # google-news  from everywhere
        if _base_url.find('www.nytimes.com') > 0:
            self.html_parse_body_tag = 'story-body-supplemental'

        # bbc-news
        if _base_url.find('www.bbc.co.uk') > 0:
            self.html_parse_body_tag = 'story-body__inner'
        if _base_url.find('www.bbc.com') > 0:
            self.html_parse_body_tag = 'story-body__inner'

        # entertainment-weekly
        if _base_url.find('ew.com') > 0:
            self.html_parse_body_tag = 'article-body__inner'

        # the-new-york-times ?
        if _base_url.find('www.nytimes.com') > 0:
            self.html_parse_body_tag = 'story-body-supplemental'

        if _base_url.find('thenextweb.com') > 0:
            self.will_del_div_tags.append('post-in-content-tags')
            self.html_parse_body_tag = 'post-body'

        if _base_url.find('www.washingtonpost.com') > 0:
            self.html_parse_body_tag = 'article-article-body'

    def display(self):
        print(self.url + '  |  ' + self.html_parse_body_tag)
        print(self.will_del_div_tags)
