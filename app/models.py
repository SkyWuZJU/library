# -*- coding=utf-8 -*-
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash  # 引入密码加密 验证方法
from flask_login import LoginManager
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128))
    phone = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u'密码属性不正确')

    def is_active(self):
        return True

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        # 增加password会通过generate_password_hash方法来加密储存

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # 在登入时,我们需要验证明文密码是否和加密密码所吻合

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    title = db.Column(db.String(64))   #name of book
    press = db.Column(db.String(64))
    year = db.Column(db.Integer)        #出版年份
    author = db.Column(db.String(64))
    price = db.Column(db.Float)
    total = db.Column(db.Integer)
    stock = db.Column(db.Integer)

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    book = db.relationship('Book',backref='category')

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True)
    cno = db.Column(db.Integer)
    name = db.Column(db.String(64))
    department = db.Column(db.String(64))
    type = db.Column(db.Boolean, default=False)

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    bno = db.Column(db.Integer,db.ForeignKey('book.id'))
    book = db.relationship('Book',backref=db.backref('records'))
    cno = db.Column(db.Integer)
    backornot = db.Column(db.Boolean, default=False)
    btime = db.Column(db.DATETIME)
    rtime = db.Column(db.DATETIME)
    username = db.Column(db.String(64))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))