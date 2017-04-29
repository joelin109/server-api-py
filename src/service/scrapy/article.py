import requests


def request_result():
    _url = 'https://newsapi.org/v1/articles'
    _params = {"sortBy": 'top', "source": 'entertainment-weekly', "apiKey": 'c53e3bc3f12b4f8ba9b7505d14a4d9f3'}
    _response = requests.get(_url, _params)
    _response_status = _response.status_code
    _response_json = _response.json()

    _result = _response_json["articles"]

    # json - list - dict
    # print(_result[1])
    print(_response_status)
    for article in _result:
        _author = article["author"]
        _title = article["title"]
        _description = article["description"]
        _url = article["url"]
        _cover_url = article["urlToImage"]
        _published_at = article["publishedAt"]

        if _published_at is None:
            print(article)
        else:
            print(_title + '|' + _published_at)

    return _response_status
