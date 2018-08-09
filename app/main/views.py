# -*- coding=utf-8 -*-
from datetime import datetime
from flask import render_template, redirect,request, url_for, flash,Response,session
from .forms import CardSearchForm,SearchBookForm,CreateCardForm,BookBackForm
from ..models import Category,Book,Card,Record
from . import main
from .. import db
import string
import random


@main.route('/')
def index():
    b = Book.query.order_by(Book.id.desc()).limit(10)
    r = Record.query.order_by(Record.btime).limit(10)
    return render_template('main/index.html', list=b,rlist = r)


#书号, 类别, 书名, 出版社, 年份, 作者, 价格, 总藏书量, 库存
@main.route('/search', methods=['GET', 'POST'])
def book_search():
    form = SearchBookForm()
    booklist = db.session.query(Book).all()
    if form.validate_on_submit():
        if form.id.data != '':
            booklist = db.session.query(Book).filter(Book.id == form.id.data).all()

        if form.category_id.data.id!=3:
            print form.category_id.data.id
            if booklist != None:
                booklist = filter(lambda book: book.category_id == form.category_id.data.id, booklist)
            else:
                booklist = db.session.query(Book).filter(Book.category_id == form.category_id.data).all()

        if form.name.data != '':
            if booklist != None:
                booklist = filter(lambda book: book.name == form.name.data, booklist)
            else:
                booklist = db.session.query(Book).filter(Book.name == form.name.data).all()

        if form.press.data != '':
            if booklist != None:
                booklist = filter(lambda book: book.press == form.press.data, booklist)
            else:
                booklist = db.session.query(Book).filter(Book.press == form.press.data).all()

        if form.yearmin.data != '':
            if booklist != None:
                booklist = filter(lambda book: int(book.year) >= int(form.yearmin.data), booklist)
            else:
                booklist = db.session.query(Book).filter(Book.year >= int(form.yearmin.data)).all()

        if form.yearmax.data != '':
            if booklist != None:
                booklist = filter(lambda book: int(book.year) <= int(form.yearmax.data), booklist)
            else:
                booklist = db.session.query(Book).filter(Book.year <= int(form.yearmax.data)).all()

        if form.author.data != '':
            if booklist != None:
                booklist = filter(lambda book: book.author == form.author.data, booklist)
            else:
                booklist = db.session.query(Book).filter(Book.author == form.author.data).all()

        if form.pricemin.data != '':
            if booklist != None:
                booklist = filter(lambda book: int(book.price) >= int(form.pricemin.data), booklist)
            else:
                booklist = db.session.query(Book).filter(int(Book.price) >= int(form.pricemin.data)).all()

        if form.pricemax.data != '':
            if booklist != None:
                booklist = filter(lambda book: int(book.price) <= int(form.pricemax.data), booklist)
            else:
                booklist = db.session.query(Book).filter(int(Book.price) <= int(form.pricemax.data)).all()

    return render_template('main/book_search.html', form=form,booklist = booklist)


@main.route('/book_show/<int:id>')
def book_show(id):
    book = db.session.query(Book).filter(Book.id == id).one()
    return render_template('main/book_show.html',book = book)

@main.route('/card_search', methods=['GET', 'POST'])
def cardsearch():
    form = CardSearchForm()
    if form.validate_on_submit():
        if db.session.query(Card).filter(Card.cno == form.cno.data).count() != 0:
            bookborrowed = db.session.query(Record).filter(Record.cno == form.cno.data).order_by(-db.desc(Record.backornot)).all()
            return render_template('main/cardsearch.html',booklist = bookborrowed,form = form)
        else:
            flash(u"借书证有误")
    return render_template('main/cardsearch.html', form = form)

@main.route('/back', methods=['GET', 'POST'])
def back():
    form = BookBackForm()
    if form.validate_on_submit():
        if db.session.query(Card).filter(Card.cno == form.cno.data).count() != 0:
            if db.session.query(Book).filter(Book.id == form.bno.data).count() != 0:
                book = db.session.query(Book).filter(Book.id == form.bno.data).one()
                if db.session.query(Record).filter(Record.bno == book.id).filter(Record.cno == form.cno.data).filter(Record.backornot == False).count() != 0:
                    record = db.session.query(Record).filter(Record.bno == book.id).filter(Record.cno == form.cno.data).filter(Record.backornot == False).first()
                    record.rtime = datetime.utcnow()
                    record.backornot = True
                    try:
                        db.session.add(record)
                        db.session.commit()
                        book.stock = book.stock + 1
                        db.session.add(book)
                        db.session.commit()
                        flash(u'还书成功')
                        return redirect(url_for('main.back'))
                    except:
                        flash(u'未知错误')
                        return redirect(url_for('main.back'))
        else:
            flash(u"借书证有误")
        return render_template('main/back.html')
    return render_template('main/back.html', form = form)

@main.route('/createcard', methods=['GET', 'POST'])
def card_create():
    form = CreateCardForm()
    if form.validate_on_submit():
        unid = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5)).replace(' ', '')
        try:
            card = Card(cno = unid,name = form.name.data,department = form.department.data,type = form.type.data)
            db.session.add(card)
            flash(u"开卡成功，卡号是{0}".format(unid))
        except:
            db.session.rollback()
            flash(u"开卡失败")
    return render_template('main/createcard.html', form = form)
