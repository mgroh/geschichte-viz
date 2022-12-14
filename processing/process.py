import requests
from xml.etree.ElementTree import fromstring
from dateutil.parser import *
from typing import TypedDict, List
import json
import tomllib


RSS_URL = 'https://www.geschichte.fm/feed/mp3/'
REFERENCES_FILE = '../data/references.toml'
JSON_FILE = '../data/geschichte.json'


class Episode(TypedDict):
    id: str
    title: str
    release_date: str
    referenced_episodes: List[str]


def load_rss():
    url = RSS_URL
    resp = requests.get(url)
    return resp.content


def rss_item_to_dict(item):
    title = item.find('title')
    (episode_id, episode_title) = title.text.split(":", 1)
    release_date_str = item.find('pubDate').text
    release_date = parse(release_date_str).strftime('%Y-%m-%d')
    return Episode(
        id=episode_id,
        title=episode_title.strip(),
        release_date=release_date,
        referenced_episodes=[]
    )


def parse_rss_to_dict(rss):
    root = fromstring(rss)
    items = root.findall('./channel/item')
    return [rss_item_to_dict(i) for i in items]


def load_references_toml():
    with open(REFERENCES_FILE, 'rb') as f:
        return tomllib.load(f)


def enrich_episode_with_references(episode, all_references):
    numeric_id = episode['id'].replace('GAG', '')
    referenced_episode_ids = ['GAG' + str(x) for x in all_references[numeric_id]]
    episode['referenced_episodes'] = referenced_episode_ids
    return episode


def write_json(episodes):
    with open(JSON_FILE, 'w', encoding='utf8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=4)


def main():
    rss = load_rss()
    all_episodes = parse_rss_to_dict(rss)
    gag_episodes = [x for x in all_episodes if x['id'].startswith('GAG')]
    references = load_references_toml()
    gag_episodes_with_references = [enrich_episode_with_references(e, references) for e in gag_episodes]
    write_json(gag_episodes_with_references)


if __name__ == '__main__':
    main()
