from bs4 import BeautifulSoup
import re


def clean_reset_body_html(soup, del_div_tags):
    # type(soups) - bs4.element.ResultSet
    _tag_figures = soup('figure')
    _tag_figure_count = len(_tag_figures)
    if _tag_figure_count >= 1:
        for _tag_figure in _tag_figures:
            _soup_tag_replace(_tag_figure)

    _soup_body = soup
    # del_div_tags = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']
    for _del_div_class in del_div_tags:
        [s.extract() for s in _soup_body.find_all("div", _del_div_class)]

    _tag_imgs = _soup_body.find_all('img')
    for img in _tag_imgs:
        if 'src' not in img.attrs:
            img.extract()
        #else:
             # print(img)

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
