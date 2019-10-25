# coding: utf-8

from data_management.tools import xml_to_dict
from data_management.model import NewsPaper, Article

import os
import requests
import configparser
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))


class LeMonde:
    def __init__(self, session):
        try:
            sql_newspaper = session.query(NewsPaper).filter(NewsPaper.name == 'Le Monde')[0]
            self.la_une = sql_newspaper.url_une
            self.newspaper_id = sql_newspaper.id
        except IndexError as e:
            config = configparser.ConfigParser()
            config.read(dir_path + '/../urls.ini')
            self.la_une = config['lemonde']['une']
            sql_newspaper = NewsPaper(name='Le Monde', url_une=self.la_une)
            session.add(sql_newspaper)
            session.commit()
            self.newspaper_id = sql_newspaper.id


    def load_une(self, session):
        xml_une = requests.get(self.la_une).text
        dict_une = xml_to_dict(xml_une)
        sql_newspaper = session.query(NewsPaper).get(self.newspaper_id)
        for item in dict_une['rss']['channel']['item']:
            article = Article(
                title=item['title'],
                publication_date=datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z'),
                description=item['description'],
                url=item['link'],
                image_url=item['enclosure']['@url'],
                newspaper=sql_newspaper
            )
            session.add(article)
        session.commit()

    def get_une(self, session):
        sql_newspaper = session.query(NewsPaper).get(self.newspaper_id)
        articles = sql_newspaper.articles
        return articles
