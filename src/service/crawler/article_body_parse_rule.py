from bs4 import BeautifulSoup, Comment
import re


def crawl_http_url_parse_rule(url):
    _del_div_tag_pool = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']

    _article_content_pool = ['mashable.com', 'www.tagesspiegel.de']
    _del_div_tag_pool2 = ['bonus-video-card', 'newsletter-signup']
    for _url_tag in _article_content_pool:
        if url.find(_url_tag) > 0:
            return 'article-content', _del_div_tag_pool2

    # www.wired.de
    if url.find('www.wired.de') > 0:
        return 'article-content', _del_div_tag_pool

    # ars - technica
    if url.find('arstechnica.com') > 0:
        return 'article-content post-page', _del_div_tag_pool

    # buzzfeed ?
    if url.find('www.buzzfeed.com') > 0:
        return '', _del_div_tag_pool

    # cnn
    if url.find('www.cnn.com') > 0:
        return 'zn-body__paragraph', _del_div_tag_pool

    # google-news  from everywhere
    if url.find('www.nytimes.com') > 0:
        return 'story-body-supplemental', _del_div_tag_pool

    # bbc-news
    if url.find('www.bbc.co.uk') > 0:
        return 'story-body__inner', _del_div_tag_pool
    if url.find('www.bbc.com') > 0:
        return 'story-body__inner', _del_div_tag_pool

    # entertainment-weekly
    if url.find('ew.com') > 0:
        return 'article-body__inner', _del_div_tag_pool

    # the-new-york-times ?
    if url.find('www.nytimes.com') > 0:
        return 'story-body-supplemental', _del_div_tag_pool

    if url.find('thenextweb.com') > 0:
        return 'post-body', _del_div_tag_pool

    return '', {}


def crawl_http_article_body_html(soup, del_div_tags):
    # type(soups) - bs4.element.ResultSet
    _tag_figures = soup('figure')
    _tag_figure_count = len(_tag_figures)
    if _tag_figure_count >= 1:
        for _tag_figure in _tag_figures:
            _soup_tag_replace(_tag_figure)

    _soup_body = soup
    for element in _soup_body(text=lambda text: isinstance(text, Comment)):
        element.extract()

    _del_h5_tags = ['figcaption', 'script', 'aside', 'video', 'blockquote']
    for _del_h5_tag in _del_h5_tags:
        [s.extract() for s in _soup_body(_del_h5_tag)]

    # del_div_tags = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']
    for _del_div_class in del_div_tags:
        [s.extract() for s in _soup_body.find_all("div", _del_div_class)]

    _del_div_re_classes = ['hidden']
    for _del_div_re_class in _del_div_re_classes:
        [s.extract() for s in _soup_body.find_all(attrs={'class': re.compile(r'' + _del_div_re_class)})]

    _tag_imgs = _soup_body.find_all('img')
    for img in _tag_imgs:
        if 'src' in img.attrs:
            print(img)
        else:
            img.extract()

    return _soup_body


def _soup_tag_replace(old_tag):
    _tag_img = old_tag.img
    if _tag_img.__class__.__name__ != 'NoneType':

        _img_src = _tag_img["src"]
        # print(_tag_img.attrs)
        if 'style' in _tag_img.attrs:
            print(_tag_img.attrs["style"])

        _new_soup = BeautifulSoup()
        _new_tag_div = _new_soup.new_tag('div')
        _new_tag_div['style'] = 'text-align: center'
        _new_tag_img = _new_soup.new_tag('img')
        _new_tag_img['src'] = _img_src
        _new_tag_img['style'] = 'height: auto; max-width: 100%'
        _new_tag_p = _new_soup.new_tag('p')
        _new_tag_p_n = _new_soup.new_tag('p')
        _new_tag_div.insert(0, _new_tag_p)
        _new_tag_div.insert(0, _new_tag_img)
        _new_tag_div.insert(0, _new_tag_p_n)

        old_tag.replaceWith(_new_tag_div)

    else:
        old_tag.extract()
