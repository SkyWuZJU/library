# -*- coding=utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, SubmitField, PasswordField, TextAreaField,IntegerField,FloatField
from wtforms.validators import Required, length, Regexp, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Category
from flask_pagedown.fields import PageDownField


#书号, 类别, 书名, 出版社, 年份, 作者, 价格, 总藏书量, 库存
class SearchBookForm(FlaskForm):
    id = StringField(u'填写书的编号:')
    category_id = QuerySelectField(u'分类', query_factory=lambda: Category.query.all(
    ), get_pk=lambda a: str(a.id), get_label=lambda a: (a.name))
    name = StringField(u'书名')
    press = StringField(u'出版社')
    yearmin = StringField(u'年份min')
    yearmax = StringField(u'年份max')
    author = StringField(u'作者')
    pricemin = StringField(u'价格min')
    pricemax = StringField(u'价格max')
    submit = SubmitField(u'提交')

class CreateCardForm(FlaskForm):
    name = StringField(u'* 填写你的名字:', validators=[Required()])
    department = StringField(u'* 填写你的单位:', validators=[Required()])
    type = SelectField(u'* 选择你的身份',choices=[('0', u'学生'), ('1', u'老师')], )
    submit = SubmitField(u'提交')

class CardSearchForm(FlaskForm):
    cno = IntegerField(u'* 填写你的借书证:', validators=[Required()])
    submit = SubmitField(u'提交')

class BookBackForm(FlaskForm):
    cno = IntegerField(u'* 填写你的借书证:', validators=[Required()])
    bno = IntegerField(u'* 填写书的编号:', validators=[Required()])
    submit = SubmitField(u'提交')