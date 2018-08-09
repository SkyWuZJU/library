# -*- coding=utf-8 -*-
from datetime import datetime

from flask import render_template, redirect, url_for, flash,request
from flask_login import login_required, login_user, logout_user,current_user
from app.admin.forms import EditBookForm,PostBookForm,PostCategoryForm,EditCategoryForm,LogForm, RegistrationForm,BorrowBookForm,AddBook
from app.admin import admin
from app import db
from app.models import User,Category,Book,Card,Record
import xlrd


@admin.route('/', methods=['GET', 'POST'])
def index():
	return render_template('admin/index.html',  current_time=datetime.utcnow())

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LogForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin.welcome'))
        flash(u'用户密码不正确')

    return render_template('admin/login.html', form=form,current_time=datetime.utcnow())

@admin.route('/borrow/<int:id>', methods=['GET', 'POST'])
@login_required
def Borrow(id):
    form = BorrowBookForm(bno = id)
    if form.validate_on_submit():
        if db.session.query(Card).filter(Card.cno == form.cno.data).count() != 0:
            if db.session.query(Book).filter(Book.id == form.bno.data).filter(Book.stock>0).count() != 0:
                book = db.session.query(Book).filter(Book.id == form.bno.data).filter(Book.stock>0).one()
                record = Record(bno = book.id,cno = form.cno.data,btime = datetime.utcnow(),username = current_user.name)
                try:
                    db.session.add(record)
                    db.session.commit()
                    book.stock = book.stock-1
                    db.session.add(book)
                    db.session.commit()
                    flash(u'借书成功')
                    return redirect(url_for('admin.borrow'))
                except:
                    flash(u'未知错误')
                    return redirect(url_for('admin.borrow'))
            flash(u'卡号错误或者库存不足')
    return render_template('admin/borrow.html', form=form)

@admin.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    form = BorrowBookForm()
    if form.validate_on_submit():
        if db.session.query(Card).filter(Card.cno == form.cno.data).count() != 0:
            if db.session.query(Book).filter(Book.id == form.bno.data).filter(Book.stock>0).count() != 0:
                book = db.session.query(Book).filter(Book.id == form.bno.data).filter(Book.stock>0).one()
                record = Record(bno = book.id,cno = form.cno.data,btime = datetime.utcnow(),username = current_user.name)
                try:
                    db.session.add(record)
                    db.session.commit()
                    book.stock = book.stock-1
                    db.session.add(book)
                    db.session.commit()
                    flash(u'借书成功')
                    return redirect(url_for('admin.borrow'))
                except:
                    flash(u'未知错误')
                    return redirect(url_for('admin.borrow'))
            flash(u'卡号错误或者库存不足')
    return render_template('admin/borrow.html', form=form)

@admin.route('/record', methods=['GET', 'POST'])
@login_required
def record():
    record = db.session.query(Record).all()
    return render_template('admin/record.html',record = record)

@admin.route('/register', methods=['GET', 'POST'])
def register():
    register_key = 'zhucema'
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registerkey.data != register_key:
            flash(u'注册码不符，请返回重试')
            return redirect(url_for('admin.register'))
        else:
            if form.password.data != form.password2.data:
                flash(u'两次输入密码不一')
                return redirect(url_for('admin.register'))
            else:
                try:
                    user = User(username=form.username.data, password=form.password.data,name = form.name.data,phone = form.phone.data)
                    print(user.password_hash)
                    print(user.username)
                    db.session.add(user)
                    print('done')
                    print('done')
                    flash(u'您已经成功注册')
                    return redirect(url_for('admin.login'))
                except:
                    db.session.rollback()
                    flash(u'用户名已存在')
    return render_template('admin/register.html', form=form,current_time=datetime.utcnow())

@admin.route('/welcome')
@login_required
def welcome():
    return render_template('admin/welcome.html',current_time=datetime.utcnow())

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = PostBookForm()
    alist = Book.query.order_by(Book.id.desc()).all()
    if form.validate_on_submit():
        book = Book(title=form.title.data, category_id=str(form.category_id.data.id),
                          press=form.press.data,year = form.year.data,author = form.author.data,price = form.price.data,total = form.total.data,stock = form.total.data)
        db.session.add(book)
        flash(u'书籍添加成功')
        return redirect(url_for('admin.book'))
    return render_template('admin/book.html', form=form,list=alist)

@admin.route('/addbook', methods=['GET', 'POST'])
@login_required
def addbook():
    form = AddBook()
    data = xlrd.open_workbook('test.xls')
    table = data.sheets()[0]
    if form.validate_on_submit():
        for rownum in range(table.nrows):
            infolist = table.row_values(rownum)
            try:
                book = Book(title=infolist[0], category_id=str(form.category_id.data.id),
                            press=infolist[1], year=infolist[2], author=infolist[4], price=infolist[3],
                            total=100, stock=100)
                db.session.add(book)
                print u'书籍添加成功'
            except:
                db.session.rollback()
    return render_template('admin/book.html', form=form)

@admin.route('/cardmanager', methods=['GET', 'POST'])
@login_required
def cardmgr():
    card = db.session.query(Card).order_by(Card.id.desc()).all()
    return render_template("admin/card.html",card=card)

@admin.route('/card/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def card_edit(id):
    if db.session.query(Card).filter(Card.cno == id).count() != 0:
        bookborrowed = db.session.query(Record).filter(Record.cno == id).all()
        return render_template('main/borrowed.html',booklist = bookborrowed)
    return render_template('main/borrowed.html', booklist=None)

@admin.route('/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def book_edit(id):
    ar = db.session.query(Book).filter(Book.id == id).one()
    form = EditBookForm(title=ar.title,press=ar.press,category_id=ar.category_id,year = ar.year,author = ar.author,price = ar.price,total = ar.total,stock = ar.total)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            dar = Book.query.get_or_404(id)
            try:
                db.session.delete(dar)
                db.session.commit()
                return redirect(url_for('admin.book'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.book_edit', id=id))
        elif form.delete.data == "":
            dar = Book.query.get_or_404(id)
            dar.title = form.title.data
            dar.press = form.press.data
            dar.category_id=str(form.category_id.data.id)
            dar.year = form.year.data
            dar.author = form.author.data
            dar.price = form.price.data
            dar.total = form.total.data
            dar.stock = form.total.data
            try:
                db.session.add(dar)
                db.session.commit()
                return redirect(url_for('admin.book'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.book_edit', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.book_edit', id=id))
    return render_template("admin/book_edit.html", form=form, id=ar.id)

@admin.route('/category', methods=['GET', 'POST'])
def category():
    clist = Category.query.all()
    form = PostCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        flash(u'分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category.html', form=form, list=clist)

@admin.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def category_edit(id):
    ca = db.session.query(Category).filter(Category.id == id).one()
    form = EditCategoryForm(name=ca.name)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            dca = Category.query.get_or_404(id)
            try:
                db.session.delete(dca)
                db.session.commit()
                return redirect(url_for('admin.category'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.category_edit', id=id))
        elif form.delete.data == "":
            dca = Category.query.get_or_404(id)
            dca.name = form.name.data
            try:
                db.session.add(dca)
                db.session.commit()
                return redirect(url_for('admin.category'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.category_edit', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.category_edit', id=id))
    return render_template("admin/category_edit.html", form=form, id=ca.id)

@admin.route('/modify/<int:id>', methods=['GET', 'POST'])
@login_required
def modify(id):
    re = db.session.query(Record).filter(Record.id == id).one()
    form = EditRecordForm(comment=re.comment,verify=re.verify)
    if form.validate_on_submit():
        if form.delete.data == u"确认删除":
            cord = Record.query.get_or_404(id)
            try:
                db.session.delete(cord)
                db.session.commit()
                return redirect(url_for('admin.record'))
            except:
                flash(u'删除失败，请联系管理员。')
                return redirect(url_for('admin.modify', id=id))
        elif form.delete.data == "":
            cord = Record.query.get_or_404(id)
            cord.comment = form.comment.data
            if form.verify.data:
                cord.verify = True
            else:
                cord.verify = False
            try:
                db.session.add(cord)
                db.session.commit()
                return redirect(url_for('admin.record'))
            except:
                flash(u'提交失败')
                return redirect(url_for('admin.modify', id=id))
        else:
            flash(u'删除栏输入有误，请重新输入')
            return redirect(url_for('admin.modify', id=id))
    return render_template("admin/modify.html", form=form, id=re.id)