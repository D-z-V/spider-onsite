from forms import LoginForm, RegisterForm, BookForm, DeleteForm
from flask import Flask, render_template, abort, request, session
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import datetime

app = Flask(__name__,template_folder='templates')

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(20), nullable=False)
    book_author = db.Column(db.String(20), nullable=False)
    book_price = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('books', lazy=True))

db.create_all()

@app.route('/home', methods=['GET', 'POST'])
def home():
    form = BookForm()
    del_form = DeleteForm()

    if 'user_id' in session:
        if form.validate_on_submit():
            book_id = Book.query.count() + 1;
            book = Book(book_id = book_id, book_name=form.book_name.data, book_author=form.book_author.data, book_price=form.book_price.data, date_added=datetime.datetime.now(), user_id=session['user_id'])
            db.session.add(book)
            db.session.commit()
            return redirect(url_for('home'))

        if del_form.validate_on_submit():
            del_book = Book.query.filter_by(book_id=del_form.book_id.data).first()
            db.session.delete(del_book)
            db.session.commit()
            return redirect(url_for('home'))

        books = Book.query.filter_by(user_id=session['user_id']).all()
        return render_template('home.html', form=form, books=books, del_form = del_form)
    else:
        return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session['user'] = user.full_name
                session['user_id'] = user.user_id
                return redirect(url_for('home'))
            else:
                return render_template('login.html', form=form, error='Wrong password')
        else:
            return render_template('login.html', form=form, error='User not found')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_id = User.query.count() + 1
            full_name = form.full_name.data
            email = form.email.data
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
            if User.query.filter_by(email=email).first():
                return render_template('signup.html', form=form, error='Email already exists')
            new_user = User(user_id=user_id, full_name=full_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', form=form)
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)