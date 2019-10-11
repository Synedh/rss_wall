from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    description = Column(String)
    image_url = Column(String)
    newspaper_id = Column(Integer, ForeignKey('newspaper.id'))

    newspaper = relationship('NewsPaper', back_populates='articles')

    def __repr__(self):
        return '<Article(title=%s, publication_date=%s, newspaper=%s)>' % (self.title, self.publication_date, self.newspaper)


class NewsPaper(Base):
    __tablename__ = 'newspaper'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url_une = Column(String, unique=True, nullable=False)

    articles = relationship('Article', back_populates='newspaper')

    def __repr__(self):
        return '<NewsPaper(name=%s)>' % (self.name)
