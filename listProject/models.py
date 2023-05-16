from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from listProject import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Item(db.Model):
    # 主键 id
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    title = db.Column(db.String(60))
    # 链接
    url = db.Column(db.String(256))
    # 标签 MOVIE/BOOK/STORE/PLACE
    tag = db.Column(db.String(10))
    # 状态 WANT/USED
    state = db.Column(db.String(10))
