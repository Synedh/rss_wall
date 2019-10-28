import os
from flask import Flask, render_template
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from data_management.model import Article, NewsPaper
from data_management.lemonde import LeMonde

app = Flask(__name__)
app.debug = True
dir_path = os.path.dirname(os.path.realpath(__file__))
engine = create_engine('sqlite:///' + dir_path + '/../account.db', echo=True)
Session = sessionmaker(bind=engine)

@app.route('/')
@app.route('/une/')
def une():
    session = Session()
    articles = session.query(Article).order_by(Article.publication_date.desc())

    return render_template('index.html', articles=articles)