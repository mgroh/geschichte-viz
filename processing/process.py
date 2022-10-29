import requests


RSS_URL = 'https://www.geschichte.fm/feed/mp3/'
RSS_FILE = '../data/geschichte.xml'


def load_rss():
    url = RSS_URL
    resp = requests.get(url)
    with open(RSS_FILE, 'wb') as f:
        f.write(resp.content)


if __name__ == '__main__':
    load_rss()
