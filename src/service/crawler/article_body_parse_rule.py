from bs4 import BeautifulSoup, Comment
import re


def crawl_http_url_parse_rule(url):
    # ars - technica
    if url.find('arstechnica.com') > 0:
        return 'article-content post-page'

    # buzzfeed ?
    if url.find('www.buzzfeed.com') > 0:
        return ''

    # cnn
    if url.find('www.cnn.com') > 0:
        return 'zn-body__paragraph'

    # der-tagesspiegel ?
    if url.find('www.tagesspiegel.de') > 0:
        return 'article-content'

    # google-news  from everywhere
    if url.find('www.nytimes.com') > 0:
        return 'story-body-supplemental'

    # bbc-news
    if url.find('www.bbc.co.uk') > 0:
        return 'story-body__inner'
    if url.find('www.bbc.com') > 0:
        return 'story-body__inner'

    # entertainment-weekly
    if url.find('ew.com') > 0:
        return 'article-body__inner'

    # the-new-york-times ?
    if url.find('www.nytimes.com') > 0:
        return 'story-body-supplemental'

    # wired-de
    if url.find('www.wired.de') > 0:
        return 'article-content'

    return ''


def crawl_http_article_body_html(soup):
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

    _del_div_classes = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']
    for _del_div_class in _del_div_classes:
        [s.extract() for s in _soup_body.find_all("div", _del_div_class)]

    _del_div_re_classes = ['hidden']
    for _del_div_re_class in _del_div_re_classes:
        [s.extract() for s in _soup_body.find_all(attrs={'class': re.compile(r'' + _del_div_re_class)})]

    # print(_soup_body.prettify())
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
