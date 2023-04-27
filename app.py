import os
import sys
import click
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


# support addr by os
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# database config
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
# hide_input 隐藏输入
# confirmation_prompt 二次确认
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating ...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating ...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


# tag 枚举，后续定义
class Item(db.Model):
    # 主键 id
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    title = db.Column(db.String(60))
    # 链接
    url = db.Column(db.String(40))
    # 标签 MOVIE/BOOK/STORE/PLACE
    tag = db.Column(db.String(10))
    # 状态 WANT/USED
    state = db.Column(db.String(10))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop db.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('DB Ready.')


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Without input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.check_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('about_me'))

        flash('Wrong input.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout.')
    return render_template('me.html')


def search(tag):
    content = Item.query.filter_by(tag=tag).all()
    print(content)
    return content


def add(input_title, input_url, input_tag, input_state):
    if not (input_title and input_url and input_tag and input_state):
        flash('Without Input.')  # 显示错误提示
        return
    elif len(input_title) > 60 or len(input_url) > 40 or len(input_tag) > 10 or len(input_state) > 10:
        flash('Wrong Input.')  # 显示错误提示
        return
    else:
        item = Item(title=input_title, url=input_url, tag=input_tag, state=input_state)
        db.session.add(item)
        db.session.commit()
        flash('Item added.')


def edit(input_id, input_title, input_url, input_tag, input_state):
    item = Item.query.get(input_id)

    if not (input_title and input_url and input_tag and input_state):
        flash('Without Input.')  # 显示错误提示
        return

    elif len(input_title) > 60 or len(input_url) > 40 or len(input_state) > 10:
        flash('Wrong Input.')  # 显示错误提示
        return

    else:
        item.title = input_title
        item.url = input_url
        item.state = input_state
        db.session.commit()
        flash('Item updated.')


def delete(input_id, input_tag):
    item = Item.query.get_or_404(input_id)
    if item.tag == input_tag:
        db.session.delete(item)
        db.session.commit()
        flash(input_tag+' '+item.title+' is deleted.')
    else:
        flash('Item tag error.')


@app.route('/')
def about_me():
    return render_template('me.html')


@app.route('/movie', methods=['GET', 'POST'])
def movie_page():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('movie_page'))
        title = request.form.get('title')
        url = request.form.get('url')
        state = request.form.get('state')
        add(input_title=title, input_url=url, input_tag='MOVIE', input_state=state)
        return redirect(url_for('movie_page'))

    movies = search('MOVIE')
    return render_template('movie.html', movies=movies)


@app.route('/book', methods=['GET', 'POST'])
def book_page():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('book_page'))
        title = request.form.get('title')
        url = request.form.get('url')
        state = request.form.get('state')
        add(input_title=title, input_url=url, input_tag='BOOK', input_state=state)
        return redirect(url_for('book_page'))

    books = search('BOOK')
    return render_template('book.html', books=books)


@app.route('/store', methods=['GET', 'POST'])
def store_page():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('store_page'))
        title = request.form.get('title')
        url = request.form.get('url')
        state = request.form.get('state')
        add(input_title=title, input_url=url, input_tag='STORE', input_state=state)
        return redirect(url_for('store_page'))

    stores = search('STORE')
    return render_template('store.html', stores=stores)


@app.route('/place', methods=['GET', 'POST'])
def place_page():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('place_page'))
        title = request.form.get('title')
        url = request.form.get('url')
        state = request.form.get('state')
        add(input_title=title, input_url=url, input_tag='place', input_state=state)
        return redirect(url_for('place_page'))

    places = search('PLACE')
    return render_template('place.html', places=places)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    item = Item.query.get_or_404(movie_id)
    if item.tag == 'MOVIE':
        if request.method == 'POST':
            title = request.form['title']
            url = request.form['url']
            state = request.form['state']
            edit(input_id=movie_id, input_title=title, input_url=url, input_state=state, input_tag='MOVIE')
            return redirect(url_for('movie_page'))

        return render_template('edit.html', item=item)
    else:
        flash('Not movie')
        return redirect(url_for('movie_page'))


@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    item = Item.query.get_or_404(book_id)
    if item.tag == 'BOOK':
        if request.method == 'POST':
            title = request.form['title']
            url = request.form['url']
            state = request.form['state']
            edit(input_id=book_id, input_title=title, input_url=url, input_state=state, input_tag='BOOK')
            return redirect(url_for('book_page'))

        return render_template('edit.html', item=item)
    else:
        flash('Not book')
        return redirect(url_for('book_page'))


@app.route('/store/edit/<int:store_id>', methods=['GET', 'POST'])
@login_required
def edit_store(store_id):
    item = Item.query.get_or_404(store_id)
    if item.tag == 'STORE':
        if request.method == 'POST':
            title = request.form['title']
            url = request.form['url']
            state = request.form['state']
            edit(input_id=store_id, input_title=title, input_url=url, input_state=state, input_tag='STORE')
            return redirect(url_for('store_page'))

        return render_template('edit.html', item=item)
    else:
        flash('Not store')
        return redirect(url_for('store_page'))


@app.route('/place/edit/<int:place_id>', methods=['GET', 'POST'])
@login_required
def edit_place(place_id):
    item = Item.query.get_or_404(place_id)
    if item.tag == 'PLACE':
        if request.method == 'POST':
            title = request.form['title']
            url = request.form['url']
            state = request.form['state']
            edit(input_id=place_id, input_title=title, input_url=url, input_state=state, input_tag='PLACE')
            return redirect(url_for('place_page'))

        return render_template('edit.html', item=item)
    else:
        flash('Not place')
        return redirect(url_for('place_page'))


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    delete(movie_id, input_tag='MOVIE')
    return redirect(url_for('movie_page'))


@app.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    delete(book_id, input_tag='BOOK')
    return redirect(url_for('book_page'))


@app.route('/store/delete/<int:store_id>', methods=['POST'])
@login_required
def delete_store(store_id):
    delete(store_id, input_tag='STORE')
    return redirect(url_for('store_page'))


@app.route('/place/delete/<int:place_id>', methods=['POST'])
@login_required
def delete_place(place_id):
    delete(place_id, input_tag='PLACE')
    return redirect(url_for('place_page'))


# 上下文处理器，每个模版都会调用return_user
@app.context_processor
def return_user():
    user = User.query.first()
    return dict(user=user)


# 404页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
