import requests
import xml.etree.ElementTree as ET
from dateutil.parser import *


RSS_URL = 'https://www.geschichte.fm/feed/mp3/'
REFERENCES_FILE = '../data/references.toml'


def load_rss():
    url = RSS_URL
    resp = requests.get(url)
    return resp.content


def rss_item_to_dict(item):
    title = item.find('title')
    (episode_id, episode_title) = title.text.split(":", 1)
    release_date_str = item.find('pubDate').text
    release_date = parse(release_date_str).strftime('%Y-%m-%d')
    return {
        'id': episode_id,
        'title': episode_title.strip(),
        'release_date': release_date,
        'related_episodes': [],
        'years': []
    }


def parse_rss_to_dict(rss):
    root = ET.fromstring(rss)
    items = root.findall('./channel/item')
    return [rss_item_to_dict(i) for i in items]


def main():
    rss = load_rss()
    d = parse_rss_to_dict(rss)
    print(d)


if __name__ == '__main__':
    main()
