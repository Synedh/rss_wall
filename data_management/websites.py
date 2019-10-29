# coding: utf-8

from data_management.tools import format_text, xml_to_dict
from data_management.model import NewsPaper, Article

import os
import requests
import xmltodict
import configparser
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))


class Website:
    def __init__(self, newspaper_name, session):
        try:
            sql_newspaper = session.query(NewsPaper).filter(NewsPaper.name == newspaper_name)[0]
            self.la_une = sql_newspaper.url_une
            self.newspaper_id = sql_newspaper.id
        except IndexError as e:
            config = configparser.ConfigParser()
            config.read(dir_path + '/../urls.ini')
            self.la_une = config[format_text(newspaper_name)]['une']
            sql_newspaper = NewsPaper(name=newspaper_name, url_une=self.la_une)
            session.add(sql_newspaper)
            session.commit()
            self.newspaper_id = sql_newspaper.id

    def load_une(self, session):
        xml_une = requests.get(self.la_une).text
        dict_une = xml_to_dict(xml_une)
        sql_newspaper = session.query(NewsPaper).get(self.newspaper_id)
        for item in dict_une['rss']['channel']['item']:
            if 'enclosure' in item.keys():
                image_url = item['enclosure']['@url']
                if image_url.count('#') > 0:
                    image_url = '#'.join(image_url.split('#')[:-1])
            else:
                image_url = ''
            url = item['link']
            if url.count('#') > 0:
                url = '#'.join(url.split('#')[:-1])
            article = Article(
                title=item['title'],
                publication_date=datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z'),
                description=item['description'],
                url=url,
                image_url=image_url,
                newspaper=sql_newspaper
            )
            session.add(article)
        session.commit()

    def get_une(self, session):
        sql_newspaper = session.query(NewsPaper).get(self.newspaper_id)
        articles = sql_newspaper.articles
        return articles


class LeMonde(Website):
    def __init__(self, session):
        Website.__init__(self, 'Le Monde', session)


class Liberation(Website):
    def __init__(self, session):
        Website.__init__(self, 'Libération', session)

    def load_une(self, session):
        xml_une = requests.get(self.la_une).text
        dict_une = xmltodict.parse(xml_une)
        sql_newspaper = session.query(NewsPaper).get(self.newspaper_id)
        for item in dict_une['feed']['entry']:
            url = ''
            image_url = ''
            try:
                for link in item['link']:
                        if link['@rel'] == 'alternate':
                            url = '?'.join(link['@href'].split('?')[:-1])
                        elif link['@rel'] == 'enclosure':
                            image_url = '?'.join(link['@href'].split('?')[:-1])
            except TypeError as e:
                # Only one link.
                if item['link']['@rel'] == 'alternate':
                    url = '?'.join(item['link']['@href'].split('?')[:-1])
                elif item['link']['@rel'] == 'enclosure':
                    image_url = '?'.join(item['link']['@href'].split('?')[:-1])
            try:
                description = item['summary']['#text']
            except KeyError as e:
                description = ''
            article = Article(
                title=item['title'],
                publication_date=datetime.strptime(''.join(item['updated'].rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z'),
                description=description,
                url=url,
                image_url=image_url,
                newspaper=sql_newspaper
            )
            session.add(article)
        session.commit()


class LeFigaro(Website):
    def __init__(self, session):
        Website.__init__(self, 'Le Figaro', session)


class LePoint(Website):
    def __init__(self, session):
        Website.__init__(self, 'Le Point', session)


class LeParisien(Website):
    def __init__(self, session):
        Website.__init__(self, 'Le Parisien', session)

    def load_une(self, session):
        pass
