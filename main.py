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
    status = db.Column(db.Integer(), unique=False, nullable=True)
    pagetypeid = db.Column(db.Integer(), unique=False, nullable=True)
    users = db.relationship('User_has_page', back_populates='page')



    def fetchPageTypeObject(self):
        tempObject = None
        if self.pagetypeid is None:
            tempObject = None
        elif self.pagetypeid < 3:
            tempObject = pageTypeDict[self.pagetypeid](page_idpage=self.idpage).first()
        else:
            tempObject = pageTypeDict[self.pagetypeid](page_idpage=self.idpage, type=self.pagetypeid-3).first()
        return tempObject

    # User_idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'),
    # nullable=False)
    # User = db.relationship('User',
    #    backref=db.backref('user', lazy=True))


class Fighter(db.Model):
    idfighter = db.Column(db.Integer, primary_key=True)
    fighterName = db.Column(db.String(255), unique=True, nullable=True)
    fighterAge = db.Column(db.Integer(), unique=False, nullable=True)
    fighterWeight = db.Column(db.Integer(), unique=False, nullable=True)
    fighterHeight = db.Column(db.Float(), unique=False, nullable=True)
    fighterMainHand = db.Column(db.String(1), unique=False, nullable=True)
    fighterEmail = db.Column(db.String(255), unique=False, nullable=True)
    fighterGif = db.Column(db.String(45), unique=True, nullable=True)
    fighterSex = db.Column(db.String(1), unique=False, nullable=True)
    fighterNacionality = db.Column(db.Integer(), unique=False, nullable=True)
    page_idpage = db.Column(db.Integer(), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Group(db.Model):
    idgroup = db.Column(db.Integer, primary_key=True)
    page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    type = db.Column(db.Integer,unique=False, nullable=True)
    groupName = db.Column(db.String(45), unique=True, nullable=True)
    groupLogo = db.Column(db.String(45), unique=True, nullable=True)
    groupEmail = db.Column(db.String(45), unique=True, nullable=True)
    groupcol = db.Column(db.String(45), unique=True, nullable=True)

class Group_has_fighter(db.Model):
    group_idgroup = db.Column(db.Integer(), primary_key=True, nullable=False)
    group_page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    fighter_idfighter = db.Column(db.Integer(), unique=True, nullable=False)
    fighter_page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    relationtype = db.Column(db.Integer(), unique=False, nullable=True)

class Event(db.Model):
    idevent = db.Column(db.Integer(), primary_key=True, nullable=False)
    page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    organizationName = db.Column(db.String(45), unique=False, nullable=True)
    organizationLogo = db.Column(db.String(45), unique=False, nullable=True)
    tournamentName = db.Column(db.String(45), unique=False, nullable=True)
    eventPage = db.Column(db.String(45), unique=False, nullable=True)
    eventLocation = db.Column(db.String(45), unique=False, nullable=True)

class Other(db.Model):
    idother = db.Column(db.Integer(), primary_key=True, nullable=False)
    page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    icon = db.Column(db.String(45), unique=False, nullable=True)
    content = db.Column(db.String(45), unique=False, nullable=True)


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

pageTypeDict = {
        None: None,
        0: Fighter.query.filter_by,
        1: Event.query.filter_by,
        2: Other.query.filter_by,
        3: Group.query.filter_by,
        4: Group.query.filter_by,
    }

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

@app.route("/terms")
def terms():
    return render_template("beko/terms.html")

@app.route("/page/<string:PageAddresi>", methods=["GET", "POST"])
def route_page(PageAddresi):
    thispagehastype = False

    page = Page.query.filter_by(nome=PageAddresi).first()
    user = User.query.filter_by(idUser=str(current_user).strip('<>').replace('User ','')).first()


    fighter = Fighter.query.filter_by(page_idpage=page.idpage).first()
    event = Event.query.filter_by(page_idpage=page.idpage).first()
    other = Other.query.filter_by(page_idpage=page.idpage).first()
    club = Group.query.filter_by(page_idpage=page.idpage, type=0).first()
    team = Group.query.filter_by(page_idpage=page.idpage, type=1).first()

    if fighter or event or other or club or team:
        thispagehastype = True


    if request.method == "POST":
        # defining the page type
        if User_has_page.query.filter_by(user_id=user.idUser, page_idpage=page.idpage, user_has_page_relationtype= 'o') is not None:
            if thispagehastype == False:
                if 'fighter' == request.form["name"]:
                    newfighter = Fighter()
                    newfighter.page_idpage = page.idpage
                    page.pagetypeid = 0
                    db.session.add(page)
                    db.session.add(newfighter)
                    db.session.commit()
                    return 'Behold! A new fighter has born!'
                if 'club' == request.form["name"]:
                    newclub = Group()
                    newclub.page_idpage = page.idpage
                    newclub.type = 0
                    page.pagetypeid = 4
                    db.session.add(page)
                    db.session.add(newclub)
                    db.session.commit()
                    return 'Behold! A new club has born!'
                if 'team' == request.form["name"]:
                    newteam = Group()
                    newteam.page_idpage = page.idpage
                    newteam.type = None
                    page.pagetypeid = 3
                    db.session.add(page)
                    db.session.add(newteam)
                    db.session.commit()
                    return 'Behold! A new team has born!'
                if 'event' == request.form["name"]:
                    newevent = Event()
                    newevent.page_idpage = page.idpage
                    page.pagetypeid = 1
                    db.session.add(page)
                    db.session.add(newevent)
                    db.session.commit()
                    return 'Behold! A new event has born!'
                if 'other' == request.form["name"]:
                    newother = Other()
                    newother.page_idpage = page.idpage
                    page.pagetypeid = 2
                    db.session.add(page)
                    db.session.add(newother)
                    db.session.commit()
                    return 'Behold! A new other has born!'
            else:
                print(request.form)

                if 'name' in request.form:
                    fighter.fighterName = request.form['name']
                    db.session.add(fighter)
                    db.session.commit()

                if 'email' in request.form:
                    fighter.fighterEmail = request.form['email']
                    db.session.add(fighter)
                    db.session.commit()

                if 'gif' in request.form:
                    fighter.fighterGif = request.form['gif']
                    db.session.add(fighter)
                    db.session.commit()

                if 'wieght' in request.form:
                    fighter.fighterWeight = request.form['wieght']
                    db.session.add(fighter)
                    db.session.commit()

                if 'age' in request.form:
                    fighter.fighterAge = request.form['age']
                    db.session.add(fighter)
                    db.session.commit()

                    #height = fighter.fighterWeight,
                    #mainhand = fighter.fighterMainHand,
                    #nacionality = fighter.fighterNacionality,
                    #name = fighter.fighterName,
                    #sex = fighter.fighterSex,
                    #background = page.background,
                    #header = page.header,
                    #icone = page.icone,

                return redirect('/page/'+PageAddresi)

        if User_has_page.query.filter_by(user_id=user.idUser, page_idpage=page.idpage) is not None:

            #definig page content
            typeObject = page.fetchPageTypeObject()

            print(type(typeObject))
            #if fighter:
            #    return redirect(url_for('route_page(PageAddresi)'))
            #elif event:
            #    return redirect(url_for('route_page'), page=PageAddresi)
            #elif other:
            #    return redirect(url_for('route_page'), page=PageAddresi)
            #elif club:
            #    return redirect(url_for('route_page'), page=PageAddresi)
            #elif team:
            #    return redirect(url_for('route_page'), page=PageAddresi)
    if request.method == "GET":
        if page is not None:
            # definig page content

            #typeObject = page.fetchPageTypeObject()
            #print(type(typeObject))


            if fighter:

                return render_template("beko/page/fighter.html", page=PageAddresi,
                                                                age=fighter.fighterAge,
                                                                email=fighter.fighterEmail,
                                                                gif=fighter.fighterGif,
                                                                weight=fighter.fighterWeight,
                                                                height=fighter.fighterWeight,
                                                                mainhand=fighter.fighterMainHand,
                                                                nacionality=fighter.fighterNacionality,
                                                                name=fighter.fighterName,
                                                                sex=fighter.fighterSex,
                                                                background=page.background,
                                                                header=page.header,
                                                                icone=page.icone,
                                                                relation=user,



                                       )
            elif event:
                return render_template("beko/page/event.html", page=PageAddresi)
            elif other:
                return render_template("beko/page/other.html", page=PageAddresi)
            elif club:
                return render_template("beko/page/club.html", page=PageAddresi)
            elif team:
                return render_template("beko/page/team.html", page=PageAddresi)
            else:
                flash('Select the page type at your page control panel')
                return render_template("beko/newpage.html", page=PageAddresi)
        else:
            return "This page doesn't exist."


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
            flash(', '.join(error))
            return redirect(url_for('register'))
        else:
            user = User(username=form.username.data, password=form.psw.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
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


            return "Logged in successfully."
        return "Login Failed!"

    # user = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    # db.session.add(user)
    # db.session.commit()
    return render_template('/beko/login.html')  # , form=form))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return 'You are now logged out.'

@app.route('/userselection', methods=['GET', 'POST'])
@login_required
def userselection():
    table = {'headers': ['Select', 'Editor', 'Page'],
             'contents': []
             }
    pagetype = 2
    pagesnames = session['checked']



    #for editor in pagesnames:
    for pagename in pagesnames:
        page = Page.query.filter_by(nome=pagename).first()
        for haspage in User_has_page.query.filter_by(page=page, user_has_page_relationtype="e").all():
            editor = haspage.user.username

            dic = {'Select': "☑",
                   'Editor': editor,
                   'Page': page.nome ,
                   }
            table['contents'].append(dic)

    if table['contents'] == []:
        flash("No editor to revoke edition power.")

    if request.method == "POST":
        for check in request.form:
            checkededitor = (check.split('_')[1])
            checkedpage = (check.split('_')[2])
            thispage = Page.query.filter_by(nome=checkedpage).first()
            thisuser = User.query.filter_by(username=checkededitor).first()
            haspage = User_has_page.query.filter_by(page=thispage,user=thisuser).first()
            thisuser.pages.remove(haspage)
            db.session.delete(haspage)
            db.session.add(thispage)
            db.session.add(thisuser)
            db.session.commit()
            flash(checkededitor +" editor power on " + thispage.nome +" page successfully repealed.")

        return redirect(url_for('pageadmo'))


    return render_template('beko/userhaspages.html', pagetype = pagetype, table=table)



@app.route('/shareselection', methods=['GET', 'POST'])
@login_required
def shareselection():
   form = Selectuser()

   error1 = None
   error2 = None
   selected = []
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
        searchuser = User.query.filter_by(username=form.username.data).first()
        if searchuser == None:
            flash("User name "+form.username.data+" not found.")
            error2 = ""

        if error2 == None:
            if error1 == None:
                # for each selected page, establish the share relationship with a given user
                for pagename in selected:
                    haspage = User_has_page()
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
                    flash("Page "+ pagename + " successfully shared! Congratulations!")
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
    table = {'headers': ['Select', 'Name', 'Editors', 'Status', 'Type'],
             'contents': []
             }
    checked = []
    pagetype = 0



    if request.method == "POST":
        for check in request.form:
            checked.append(check.split('_')[1])



        if checked == [("Revoke")] or checked == [('Share')]:
            flash("You must select pages first.")
            return redirect(url_for('pageadmo'))
        else:
            if ("Revoke") in checked:
                checked.remove("Revoke")
                session['checked'] = checked
                return redirect(url_for('userselection'))
            elif ("Share") in checked:
                checked.remove("Share")
                session['checked'] = checked
                return redirect(url_for('shareselection'))
            elif ("Delete") in checked:
                checked.remove("Delete")
                for check in checked:
                    page = Page.query.filter_by(nome=check).first()
                    # checking the page type and deleting content
                    fighter = Fighter.query.filter_by(page_idpage=page.idpage).first()
                    event = Event.query.filter_by(page_idpage=page.idpage).first()
                    other = Other.query.filter_by(page_idpage=page.idpage).first()
                    club = Group.query.filter_by(page_idpage=page.idpage).first()
                    if fighter is not None:
                        db.session.delete(fighter)
                    if event is not None:
                        db.session.delete(event)
                    if other is not None:
                        db.session.delete(other)
                    if club is not None:
                        db.session.delete(club)

                    flash("Page "+check+" deleted.")
                    # deleting relations
                    haspages = page.users
                    for objhaspage in haspages:
                        user = objhaspage.user
                        user.pages.remove(objhaspage)
                        page.users.remove(objhaspage)
                        db.session.delete(objhaspage)
                        db.session.add(user)
                    # finaly deleting page
                    db.session.delete(page)
                db.session.commit()
                return redirect(url_for('pageadmo'))

    for page in current_user.pages:
        # if request.method == "POST":
        #    if page.page.nome not in checked:
        #        continue
        #    else :
        #        pass
        editors = []
        # passing parameters if owner
        if page.user_has_page_relationtype == "o":
            select = "☑"

            for has_page in User_has_page.query.filter_by(user_has_page_relationtype="e").all():
                if has_page.user != current_user:
                    if page.page == has_page.page:
                        editors += [has_page.user.username]

        else:
            select = ""

        if page.page.status == 1:
            status = "Published"
        elif page.page.status == None:
            status = "Unpublished"
        elif page.page.status == 0:
            status = "Waiting aproval"

        editors = ", ".join(editors)

        if Fighter.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Fighter'
        elif Group.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thisgroup = Group.query.filter_by(page_idpage=page.page.idpage).first()
            if thisgroup.type == None:
                thistype = 'Team'
            else:
                thistype = 'Club'
        elif Event.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Event'
        elif Other.query.filter_by(page_idpage=page.page.idpage).first() is not None:
            thistype = 'Other'
        else:
            thistype = '﹃' #this symbol will construct a drop list with page options on template

        if page.user_has_page_relationtype == "o":
            dic = {'Select': select,
                   'Name': page.page.nome,
                   'Editors': editors,
                   'Status': status,
                   'Type': thistype
                   }
            table['contents'].append(dic)

    return render_template('beko/userhaspages.html', table=table, pagetype=pagetype)

@app.route("/pageadme", methods=['GET', 'POST'])
@login_required
def pageadme():
    table = {'headers': ['Select', 'Name', 'Status'],
             'contents': []
             }
    checked = []
    pagetype = 1

    if request.method == "POST":
        for check in request.form:
            #checked.append(check.split('_')[1])
            thispage = Page.query.filter_by(nome=(check.split('_')[1])).first()
            haspage = User_has_page.query.filter_by(page=thispage,user=current_user).first()
            #for haspage in haspages:
                #if haspage.user == current_user:
            current_user.pages.remove(haspage)
            db.session.delete(haspage)
            db.session.add(thispage)
            db.session.add(current_user)
            db.session.commit()
            flash("Editor power on " + check.split('_')[1] + " page successfully abdicated.")

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


        if page.page.status == 1:
            status = "Published"
        elif page.page.status == None:
            status = "Unpublished"
        elif page.page.status == 0:
            status = "Waiting aproval"

        if page.user_has_page_relationtype == "e":
            dic = {'Select': select,
                   'Name': page.page.nome,
                   'Status': status,

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

def iniciarbanco():
    #db.drop_all()
    #db.create_all()

    user1 = User(username="arbusto", password="werwer", email="jenkins@leroy.com")
    db.session.add(user1)

    user2 = User(username="tony", password="123123", email="jenkins@leroytcs.com")
    db.session.add(user2)

    fighter = Fighter(
    fighterName        = "Tornado Ferreira",
    fighterAge         = 1988,
    fighterWeight      = 90,
    fighterHeight      = 175,
    fighterMainHand    = "R",
    fighterEmail       = "johnbiritones@gmail.com",
    fighterGif         = None,
    fighterSex         = "M",
    )
    db.session.add(fighter)

    page = Page(
    nome     = "tferreira",
    header      = None,
    icone     = None,
    pagetypeid = 0,
    status = None,

    )
    db.session.add(page)

    user_page = User_has_page (
    user_id            = user1.idUser,
    page_idpage            = page.idpage,
    user_has_PageRelation  = "o",
    )

    user_page = User_has_page(
        user_id = user2.idUser,
        page_idpage=page.idpage,
        user_has_PageRelation="e",
    )

    db.session.add(user_page)

    db.session.commit()

#iniciarbanco()

app.run(debug=True, host='0.0.0.0')
