from email.policy import default
from flask import Flask, render_template, abort, request, session
from forms import LoginForm, SignUpForm, SearchForm, CommentForm, UserForm, delComment
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
import datetime
import os

app = Flask(__name__,template_folder='templates')

UPLOAD_FOLDER = 'static/videos/users/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    comment = db.Column(db.String)
    posted_by_id = db.Column(db.Integer)
    date_posted = db.Column(db.String)
    profile_pic = db.Column(db.String)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    profile_pic = db.Column(db.String, default='default.png')

class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String)
    video_path = db.Column(db.String)
    video_description = db.Column(db.String)
    video_date = db.Column(db.String)
    comment_id = db.Column(db.String, db.ForignKey('Comments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('videos', lazy=True))

db.create_all()

@app.route("/")
def home_page():    
    form = LoginForm()
    return render_template("login.html", form = form)


@app.route("/search", methods=['POST', 'GET'])
def search():
    form = SearchForm()
    users = User.query
    if form.validate_on_submit():
        search = form.search.data
        #search for all columns and return all results
        users = User.query.filter(User.full_name.contains(search) | User.email.contains(search))

        return render_template("search.html", users = users, search = search, form = form)
    else:
        return render_template("search.html", form=form, users = users)


@app.route("/profile/<int:user_id>", methods=['POST', 'GET'])
def profile(user_id):
    form = SearchForm()
    form_2 = CommentForm()
    from_3 = UserForm()
    form_4 = delComment()

    if from_3.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if from_3.profile_pic.data != None:
            profile_picture = from_3.profile_pic.data
            profile_pic_name = secure_filename(from_3.profile_pic.name)
            pic_name = str(uuid.uuid1()) + '_' + profile_pic_name
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            user.profile_pic = pic_name
            db.session.commit()
            return redirect(url_for('profile', user_id=user_id))


    users = User.query.all()
    if form_2.validate_on_submit():
        comment = form_2.comment.data
        comment = Comments(user_id = user_id, 
                            comment = comment, 
                            posted_by = users[session['user']-1].full_name, 
                            profile_pic = users[session['user']-1].profile_pic, 
                            posted_by_id = session['user'],
                            date_posted = datetime.datetime.now().strftime("%B %d, %Y")
                        )

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('profile', user_id = user_id))

    comments = Comments.query.filter_by(user_id = user_id)

    
    if form_4.validate_on_submit():
        comment_id = request.form.get('comment_id')
        comment = Comments.query.get(comment_id)
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('profile', user_id = user_id))


    for i in range (len(users)):
        if (users[i].id==user_id):
           return render_template("profile.html", user = users[i], form = form, comments = comments)
    else:
        abort(404, description="No Profile was Found with the given ID")                     


@app.route("/signup", methods=["POST", "GET"])
def signup():
    status = 0
    form = SignUpForm()
    if form.validate_on_submit():
        status = 1
        new_user = User(id = len(User.query.all())+1, 
                            full_name =  form.full_name.data, 
                            email = form.email.data, 
                            password = form.password.data, 
                        )

        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, status=3)
        finally:
            db.session.close()
        return render_template("signup.html",form = form, status=status)
    return render_template("signup.html",form = form, status=status)


@app.route("/login", methods=["GET", "POST"])
def login():
    session['user'] = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, status=0)
        else:
            session['user'] = user.id
            return redirect(url_for("profile", user_id = user.id))
    return render_template("login.html", form = form)


port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
