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
    # 主键 id
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    title = db.Column(db.String(60))
    # 链接
    url = db.Column(db.String(40))
    # 标签 MOVIE/BOOK/STORE/PLACE
    tag = db.Column(db.String(20))
    # 热度
    star = db.Column(db.Integer)
    # 状态 WANT/USED
    state = db.Column(db.Integer)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop db.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('DB Ready.')


def search(tag):
    content = Item.query.filter_by(tag=tag).all()
    print(content)
    return content


@app.route('/')
def about_me():
    return render_template('me.html')


@app.route('/movie')
def search_movie():
    movies = search('MOVIE')
    return render_template('movie.html', movies=movies)


@app.route('/book')
def search_book():
    books = search('BOOK')
    return render_template('book.html', books=books)


@app.route('/store')
def search_store():
    stores = search('STORE')
    return render_template('store.html', stores=stores)


@app.route('/place')
def search_place():
    places = search('PLACE')
    return render_template('place.html', places=places)


# 上下文处理器，每个模版都会调用return_user
@app.context_processor
def return_user():
    user = User.query.first()
    return dict(user=user)


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# create fake data
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'DiuDiu'
    movies = [
        {'title': 'My Neighbor Totoro', 'url': 'https://movie.douban.com/subject/1291560/', 'tag': 'MOVIE',
         'state': 'USED'},
        {'title': 'Dead Poets Society', 'url': 'https://movie.douban.com/subject/1291548/', 'tag': 'BOOK',
         'state': 'WANT'},
        {'title': 'My Neighbor Totoro', 'url': 'https://movie.douban.com/subject/1291560/', 'tag': 'PLACE',
         'state': 'USED'},
        {'title': 'Dead Poets Society', 'url': 'https://movie.douban.com/subject/1291548/', 'tag': 'STORE',
         'state': 'WANT'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Item(title=m['title'], url=m['url'], tag=m['tag'], state=m['state'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
