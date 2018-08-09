# -*- coding=utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField,FloatField,StringField, SubmitField, PasswordField,BooleanField, TextAreaField
from wtforms.validators import Required, length, Regexp, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Category
from flask.ext.pagedown.fields import PageDownField

class LogForm(Form):
	username = StringField(u'帐号', validators=[Required(), length(1, 64)])
	password = PasswordField(u'密码', validators=[Required()])
	submit = SubmitField(u'提交')

class RegistrationForm(Form):
    username = StringField(u'用户名', validators=[Required(), length(2, 128)])
    password = PasswordField(
        u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码不一致')])
    password2 = PasswordField(u'重复密码', validators=[Required()])
    name = StringField(u'姓名', validators=[Required()])
    phone = StringField(u'手机', validators=[Required()])
    registerkey = PasswordField(u'注册码', validators=[Required()])
    submit = SubmitField(u'注册')

class PostBookForm(Form):
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
    title = StringField(u'书名', validators=[Required(), length(1, 64)])
    press = StringField(u'出版社', validators=[Required(), length(1, 64)])
    year = IntegerField(u'出版年份',validators=[Required()])
    author = StringField(u'作者', validators=[Required(), length(1, 64)])
    price = FloatField(u'价格',validators = [Required()])
    total = IntegerField(u'总库存',validators=[Required()])
    submit = SubmitField(u'发布')

class EditBookForm(Form):
    title = TextAreaField(u'更改书名为:', validators=[Required()])
    press = StringField(u'更改出版社为:', validators=[Required()])
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
    year = IntegerField(u'修改出版年份为', validators=[Required()])
    author = StringField(u'修改作者为', validators=[Required(), length(1, 64)])
    price = FloatField(u'修改价格为', validators=[Required()])
    total = IntegerField(u'修改总库存为', validators=[Required()])
    stock = IntegerField(u'修改当前库存为', validators=[Required()])
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class PostCategoryForm(Form):
    name = StringField(u'分类名', validators=[Required(), length(1, 64)])
    submit = SubmitField(u'发布')

class EditCategoryForm(Form):
    name = TextAreaField(u'更改名字为:', validators=[Required()])
    delete = StringField(u'如果你要删除这条记录，输入“确认删除”之后点击提交！否则请留空。')
    submit = SubmitField(u'提交')

class BorrowBookForm(Form):
    cno = StringField(u'输入借书证卡号')
    bno = IntegerField(u'输入书本编号')
    submit = SubmitField(u'提交')

class AddBook(Form):
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: a.name)
    submit = SubmitField(u'提交')