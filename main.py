from typing import List

from flask import Flask, escape, request, url_for, render_template, abort, flash, redirect, session
import json
from controllers import blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectFieldBase, PasswordField
from wtforms.validators import DataRequired
from flask_debug import Debug
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator, Text


app = Flask(__name__)

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:6=2Cxl{3t6}g[pD@localhost/medievalfights"""
db = SQLAlchemy(app)
nav = Nav()

login_manager = LoginManager()
login_manager.init_app(app)


class User_has_page(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.idUser'), primary_key=True)
    page_idpage = db.Column(db.Integer, db.ForeignKey('page.idpage'), primary_key=True)
    user_has_page_relationtype = db.Column(db.String(1), unique=False, nullable=True)

    user = db.relationship('User', back_populates='pages')
    page = db.relationship('Page', back_populates='users')


class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(45), unique=True, nullable=True)
    email = db.Column(db.String(45), unique=False, nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    authenticated = False
    power = db.Column(db.Integer, unique=False, nullable=True, default=None)
    pages = db.relationship('User_has_page', back_populates='user')

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUser


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(idUser=user_id).first()
    print(user)
    return user


class Page(db.Model):
    idpage = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), unique=True, nullable=False)
    icone = db.Column(db.String(45), unique=True, nullable=True)
    header = db.Column(db.String(45), unique=False, nullable=True)
    background = db.Column(db.String(45), unique=False, nullable=True)
    users = db.relationship('User_has_page', back_populates='page')

    # User_idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'),
    # nullable=False)
    # User = db.relationship('User',
    #    backref=db.backref('user', lazy=True))


class Fighter(db.Model):
    idfighter = db.Column(db.Integer, primary_key=True)
    fighterName = db.Column(db.String(255), unique=True, nullable=False)
    fighterAge = db.Column(db.Integer(), unique=False, nullable=False)
    fighterWeight = db.Column(db.Integer(), unique=False, nullable=False)
    fighterHeight = db.Column(db.Integer(), unique=False, nullable=False)
    fighterMainHand = db.Column(db.String(1), unique=False, nullable=False)
    fighterEmail = db.Column(db.String(255), unique=False, nullable=False)
    fighterGif = db.Column(db.String(45), unique=True, nullable=True)
    fighterSex = db.Column(db.String(1), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    psw = PasswordField('psw', validators=[DataRequired()])
    repassword = PasswordField('repassword', validators=[DataRequired()])
    # Agree = SelectFieldBase('', validators=[DataRequired])
    Submit: SubmitField = SubmitField('Submit')


class Addpage(FlaskForm):
    pagename = StringField('pagename', validators=[DataRequired()])
    Submit: SubmitField = SubmitField('Submit')

class Selectuser(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    Submit: SubmitField = SubmitField('Submit')

def frontend_top():
    tempNav = Navbar(title="Medieval Fights")

    tempNav.items += [
        View('Home', 'index'),
        View('Clubs', 'index'),
        View('Fighters', 'index'),
        View('Teams', 'index'),
        View('Events', 'index'),
        View('Sports', 'index'),
        #View('Latest News', 'news', {'page': 1}),
    ]

    if current_user.is_authenticated:
        tempNav.items += [Subgroup(current_user.username,
                            # View('Perfil', 'frontend.user_profile'),
                             View('Logout', 'logout'),
                             )]
    else:
        tempNav.items += [Subgroup('Visitante',
                                   View('Login', 'login'))]
    return tempNav


# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', frontend_top)
nav.init_app(app)
# db.create_all()


# club = {
#    "rosadeferro" : {
#
#    }
# }

# cliente = {
#    0 : {
#        "nome": "arbusto",
#        "sobrenome": "gustavo",
#        "idade": 10,
#        "telefone": 22441000
#    }
# }

# @app.route('/')#default = GET
# def hello():
#    name = request.args.get("name", "World")
#    return f'Hello, {escape(name)}!'

# @app.route('/nome/<meunome>')
# def name(meunome):
#    return 'Hello, %s!' % meunome, 200

# @app.route('/cliente/<int:id>', methods=["GET","POST"])
# def clienteAPI(id=-1):
#    if request.method == "GET":
#        if id in cliente.keys():
#            return json.dumps(cliente[id]), 200
#        else:
#            return "", 401

#    elif request.method == "POST":
#        return "", 403
#    else:
#        return "", 404


@app.route("/")
def index():
    return render_template("beko/index.html")


@app.route("/page/<string:PageAddresi>", methods=["GET"])
def route_page(PageAddresi):
    if request.method == "GET":
        # q = Page.query.all()
        # i = 0
        # strings = ["tornadoferreira", "stevejobs"]
        # for page in q:
        #    print(page)
        #    page.PageAddres = strings[i]
        #    i+=1
        #    db.session.add(page)
        #    db.session.commit()
        page = Page.query.filter_by(nome=PageAddresi).all()
        print(PageAddresi)
        if page:
            return render_template("beko/fighter.html")
        else:
            return "", 401


@app.route("/testelog")
@login_required
def testelog():
    return "Hello, " + current_user.username + "!", 200


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MyForm()
    error = []

    # print (form.validate_on_submit())
    if form.validate_on_submit():
        if form.psw.data != form.repassword.data:
            error.append("The passwords do not match")
        if User.query.filter_by(username=form.username.data).first() is not None:
            error.append("The user already exists")
        if User.query.filter_by(email=form.email.data).first() is not None:
            error.append("The email already exists")
        if form.email.data.find('@') == -1:
            error.append("The email is invalid")

        if error:
            flash("Error!")
            flash(', '.join(error))
            return redirect(url_for('register'))
        else:
            user = User(username=form.username.data, password=form.psw.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(request.args.get("next") or url_for('index'))
    return render_template('/beko/userregisterwtf.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    # form = LoginForm()
    # if form.validate_on_submit():
    if request.method == "POST":

        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and request.form['password'] == user.password:
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)



            #next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #    return abort(400)

            return 'Logged in successfully.'
        return "Login Failed!"

    # user = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    # db.session.add(user)
    # db.session.commit()
    return render_template('/beko/login.html')  # , form=form))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out."


@app.route('/shareselection', methods=['GET', 'POST'])
@login_required
def shareselection():
   form = Selectuser()
   haspage = User_has_page()
   error1 = None
   error2 = None
   if form.validate_on_submit():
        # retrieve the selected page names from pageadm stored in the session cookie
        selected = session['checked']

        # verifying if the selected user already has the editor power
        for pagename in selected:
            user = User.query.filter_by(username=form.username.data).first()
            page = Page.query.filter_by(nome=pagename).first()
            if True in [user == haspage.user for haspage in page.users]:
                flash("User "+user.username+" already has the editor power on "+page.nome)
                error1 = ""

        # verifying if the user exists
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            flash("User name "+form.username.data+" not found.")
            error2 = ""

        if error2 == None:
            if error1 == None:
                # for each selected page, establish the share relationship with a given user
                for pagename in selected:
                    user = User.query.filter_by(username=form.username.data).first()
                    page = Page.query.filter_by(nome=pagename).first()
                    haspage.page = page
                    haspage.user_has_page_relationtype = "e"
                    haspage.user_id = user.idUser
                    user.pages.append(haspage)

                    # update objects in the database
                    db.session.add(haspage)
                    db.session.add(user)
                    db.session.add(page)
                    db.session.commit()
                    flash("Page successfully shared! Congratulations!")
            else:
                return redirect(url_for('pageadmo'))
        else:
            return redirect(url_for('shareselection'))

        # return to the user pages administration page
        return redirect(url_for('pageadmo'))

    # renders the webpage containing the form to select the target user to share pages with
   return render_template('beko/userselectuserstoshare.html', form = form)

@app.route("/pageadmo", methods=['GET', 'POST'])
@login_required
def pageadmo():
    table = {'headers': ['Select', 'Name', 'Editors'],
             'contents': []
             }
    checked = []
    pagetype = 0


    if request.method == "POST":
        for check in request.form:
            checked.append(check.split('_')[1])
        session['checked'] = checked

        return redirect(url_for('shareselection'))

    for page in current_user.pages:
        # if request.method == "POST":
        #    if page.page.nome not in checked:
        #        continue
        #    else :
        #        pass

        # passing parameters if owner
        if page.user_has_page_relationtype == "o":
            select = "☑"
            editors = []
            for has_page in User_has_page.query.filter_by(user_has_page_relationtype="e").all():
                if has_page.user != current_user:
                    if page.page == has_page.page:
                        editors += [has_page.user.username]

        else:
            select = ""


        editors = ", ".join(editors)

        if page.user_has_page_relationtype == "o":
            dic = {'Select': select,
                   'Name': page.page.nome,
                   'Editors': editors,
                   }
            table['contents'].append(dic)

    return render_template('beko/userhaspages.html', table=table, pagetype=pagetype)

@app.route("/pageadme", methods=['GET', 'POST'])
@login_required
def pageadme():
    table = {'headers': ['Select', 'Name'],
             'contents': []
             }
    checked = []
    pagetype = 1

    if request.method == "POST":
        for check in request.form:
            checked.append(check.split('_')[1])
            flash("Editor power on " + check.split('_')[1] + " page successfully abdicated.")
        session['checked'] = checked



        return redirect(url_for('pageadme'))

    for page in current_user.pages:
        # if request.method == "POST":
        #    if page.page.nome not in checked:
        #        continue
        #    else :
        #        pass

        if page.user_has_page_relationtype == "e":
            select = "☑"
        else:
            select = ""

        if page.user_has_page_relationtype == "e":
            dic = {'Select': select,
                   'Name': page.page.nome,

                   }
            table['contents'].append(dic)



    return render_template('beko/userhaspages.html', table=table, pagetype=pagetype)


@app.route("/pageregister", methods=['GET', 'POST'])
@login_required
def pageregister():
    pageform = Addpage()
    haspage = User_has_page()
    if pageform.validate_on_submit():
        if Page.query.filter_by(nome=pageform.pagename.data).first() is not None:
            flash("Sorry. This page already exists!")
        else:
            page = Page(nome=pageform.pagename.data)
            haspage.page = page
            haspage.user_has_page_relationtype = "o"
            haspage.user = current_user
            db.session.add(page)
            current_user.pages.append(haspage)
            db.session.add(haspage)
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('pageadmo'))

    return render_template('/beko/userregisterpage.html', form=pageform)

@app.route('/pagecontrol')
@login_required
def pagecontrol():

    thisUserPower = current_user.power
    return render_template('/beko/pagecontrol.html', thisUserPower=thisUserPower)

# def iniciarbanco():
# user1 = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
# db.session.add(user1)

# user2 = User(UserName="tony", Password="123123", Email="jenkins@leroytcs.com")
# db.session.add(user2)

# fighter = Fighter(
# FighterName        = "Tornado Ferreira",
# FighterAge         = 1988,
# FighterWeight      = 90,
# FighterHeight      = 175,
# FighterMainHand    = "R",
# FighterEmail       = "johnbiritones@gmail.com",
# FighterGif         = None,
# FighterSex         = "M",
# )
# db.session.add(fighter)

# page = Page(
# PageAddres     = "tferreira",
# PagePhoto      = None,
# PageHeader     = None,
# PageBackground = None,
# )
# db.session.add(page)

# user_page = User_has_page (
# User_idUser            = 1,
# Page_idPage            = page.idPage,
# Page_User_idUser       = None,
# Page_Club_idClub       = None,
# Page_Fighter_idFighter = fighter.idFighter,
# user_has_PageRelation  = "C",
# )
# db.session.add(user_page)

# db.session.commit()

# iniciarbanco()

app.run(debug=True, host='0.0.0.0')
