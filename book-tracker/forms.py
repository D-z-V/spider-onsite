from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Email, EqualTo, email_validator

class DeleteForm(FlaskForm):
    book_id = StringField('Book ID', validators=[InputRequired()])
    delete = SubmitField('Delete')

class LoginForm(FlaskForm):
    email = StringField('Fullname', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    full_name = StringField('Fullname', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class BookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[InputRequired()])
    book_author = StringField('Book Author', validators=[InputRequired()])
    book_price = StringField('Book Price', validators=[InputRequired()])
    date_added = StringField('Date Added', validators=[InputRequired()])
    submit = SubmitField('Add Book')