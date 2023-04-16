import os
import sys
import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# support addr by os
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# database config
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


# tag 枚举，后续定义
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    url = db.Column(db.String(40))
    tag = db.Column(db.String(20))
    star = db.Column(db.Integer)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop db.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('DB Ready.')


@app.route('/')
def hello():
    user = User.query.first()
    movies = Item.query.filter_by(tag='MOVIE').all()
    return render_template('index.html', user=user, movies=movies)


# create fake data
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'DiuDiu'
    movies = [
        {'title': 'My Neighbor Totoro', 'url': 'https://movie.douban.com/subject/1291560/', 'tag': 'MOVIE'},
        {'title': 'Dead Poets Society', 'url': 'https://movie.douban.com/subject/1291548/', 'tag': 'MOVIE'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Item(title=m['title'], url=m['url'], tag=m['tag'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
