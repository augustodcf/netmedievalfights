from typing import List

from flask import Flask, escape, request, url_for, render_template, abort, flash, redirect, session
import json
from controllers import blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectFieldBase, PasswordField, DateField
from wtforms.validators import DataRequired
from flask_debug import Debug
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator, Text
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir)+os.sep+"static/page"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])

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
    fighterWeight = db.Column(db.Float(), unique=False, nullable=True)
    fighterHeight = db.Column(db.Float(), unique=False, nullable=True)
    fighterMainHand = db.Column(db.String(1), unique=False, nullable=True)
    fighterEmail = db.Column(db.String(255), unique=False, nullable=True)
    fighterGif = db.Column(db.String(255), unique=True, nullable=True)
    fighterSex = db.Column(db.String(1), unique=False, nullable=True)
    fighterNacionality = db.Column(db.String(30), unique=False, nullable=True)
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
    group_has_fighter_entrance = db.Column(db.Date(), primary_key=True, nullable=True)
    group_has_fightercol_exit = db.Column(db.Date(), unique=False, nullable=True)

class Event(db.Model):
    idevent = db.Column(db.Integer(), primary_key=True, nullable=False)
    page_idpage = db.Column(db.Integer(), unique=True, nullable=False)
    organizationName = db.Column(db.String(45), unique=False, nullable=True)
    organizationLogo = db.Column(db.String(45), unique=False, nullable=True)
    tournamentName = db.Column(db.String(45), unique=False, nullable=True)
    eventPage = db.Column(db.String(45), unique=False, nullable=True)
    eventLocation = db.Column(db.String(45), unique=False, nullable=True)

class Stage(db.Model):
    idStage = db.Column(db.Integer(), primary_key=True, nullable=False)
    event_idevent = db.Column(db.Integer(), unique=False, nullable=False)
    event_page_idpage = db.Column(db.Integer(), unique=False, nullable=False)
    stageName = db.Column(db.String(45), unique=False, nullable=True)

class Fight(db.Model):
    idfight  = db.Column(db.Integer(), primary_key=True, nullable=False)
    stage_idstage  = db.Column(db.Integer(), unique=True, nullable=False)
    fightdate = db.Column(db.Date(), unique=False, nullable=True)
    judge_idjudge = db.Column(db.Integer(), unique=False, nullable=True)

class Fight_has_group(db.Model):
    fight_idfight = db.Column(db.Integer(), primary_key=True, nullable=False)
    fight_stage_idStage = db.Column(db.Integer(), primary_key=True, nullable=False)
    fight_stage_Event_page_idpage = db.Column(db.Integer(), unique=False, nullable=True)
    fight_stage_Event_id = db.Column(db.Integer(), unique=False, nullable=True)
    group_idgroup = db.Column(db.Integer(), primary_key=True, nullable=False)
    group_page_idpage = db.Column(db.Integer(), primary_key=True, nullable=False)
    fight_has_group_result = db.Column(db.Integer(), unique=False, nullable=True)
    idfight_has_group  = db.Column(db.Integer(), primary_key=True, nullable=False)


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

class editorform(FlaskForm):
    name = StringField()
    age = DateField()
    email = StringField()
    weight =  StringField()
    height = StringField()
    mainhand = StringField()
    nacionality = StringField()
    sex = StringField()

#def frontend_top():
#    tempNav = Navbar(title="Medieval Fights")
#
#    tempNav.items += [
#        View('Home', 'index'),
#        View('Clubs', 'index'),
#        View('Fighters', 'index'),
#        View('Teams', 'index'),
#        View('Events', 'index'),
#        View('Sports', 'index'),
#        #View('Latest News', 'news', {'page': 1}),
#    ]
#
#    if current_user.is_authenticated:
#        tempNav.items += [Subgroup(current_user.username,
#                            # View('Perfil', 'frontend.user_profile'),
#                             View('Logout', 'logout'),
#                             )]
#    else:
#        tempNav.items += [Subgroup('Visitante',
#                                   View('Login', 'login'))]
#    return tempNav


# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
#nav.register_element('frontend_top', frontend_top)
#nav.init_app(app)
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

    if page is not None:

        fighter = Fighter.query.filter_by(page_idpage=page.idpage).first()
        event = Event.query.filter_by(page_idpage=page.idpage).first()
        other = Other.query.filter_by(page_idpage=page.idpage).first()
        club = Group.query.filter_by(page_idpage=page.idpage, type=0).first()
        team = Group.query.filter_by(page_idpage=page.idpage, type=None).first()

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
                if event:

                    if 'newcontestant' in request.form:
                        newfhg = Group_has_fighter()
                        newfhg.fighter_page_idpage = request.form['newcontestant']
                        newfhg.g

                    if 'addfight' in request.form:
                        newfight = Fight()
                        stage = Stage.query.filter_by(stageName=request.form['addfight'],event_idevent=event.idevent).first()
                        newfight.stage_idstage = stage.idStage
                        db.session.add(newfight)
                        db.session.commit()

                    if 'delete' in request.form:
                        if request.form['type'] == 'Fight':
                            fighttodelete = Fight.query.filter_by(idfight=request.form['delete']).first()
                            db.session.delete(fighttodelete)
                            db.session.commit()

                        if request.form['type'] == 'Stage':
                            stagetodelete = Stage.query.filter_by(stageName=request.form['delete']).first()
                            if stagetodelete:
                                allstagefights = Fight.query.filter_by(stage_idstage=stagetodelete.idStage).all()
                                if allstagefights != []:
                                    for eachstagefight in allstagefights:
                                        if eachstagefight != None:
                                            allfhg = Fight_has_group.query.filter_by(fight_idfight=eachstagefight.idfight).all()
                                            for eachfhg in allfhg:
                                                if eachfhg != None:
                                                    db.session.delete(eachfhg)
                                            db.session.delete(eachstagefight)
                                db.session.delete(stagetodelete)
                                db.session.add(event)
                                db.session.commit()

                            else:
                                flash("Stage doesn't exists")

                        return redirect('/page/' + PageAddresi)


                    if 'stage' in request.form:
                        if Stage.query.filter_by(stageName=request.form['stage'],event_idevent=event.idevent).first():
                            flash("It can't create a stage with this name in this event. Try a different stage name.")
                        else:
                            newstage = Stage()
                            newstage.stageName = request.form['stage']
                            newstage.event_idevent = event.idevent
                            pageid = page.query.filter_by(nome = PageAddresi).first()
                            newstage.event_page_idpage = pageid.idpage
                            db.session.add(event)
                            db.session.add(newstage)
                            db.session.commit()
                            flash(newstage.stageName+" stage created.")
                    return redirect('/page/' + PageAddresi)
                if club:
                    if 'fighter' in request.form or 'capitain' in request.form or 'coach' in request.form or 'mercenary' in request.form:
                        newplayerpage = None
                        newplayer = None
                        newplayeronclub = Group_has_fighter()
                        newplayerrelation = None
                        if 'fighter' in request.form:
                            newplayerpage = Page.query.filter_by(nome=request.form['fighter']).first()
                            if newplayerpage == None:
                                flash("You must enter a fighter page name to invite to the club.")
                                return redirect('/page/' + PageAddresi)
                            newplayer = Fighter.query.filter_by(page_idpage=newplayerpage.idpage).first()
                        if request.form['entrance'] == '':
                            flash("You must enter a entrance date to invite to the club.")
                            return redirect('/page/' + PageAddresi)
                        newplayeronclub.group_has_fighter_entrance = request.form['entrance']
                        newplayeronclub.fighter_idfighter = newplayer.idfighter
                        newplayeronclub.fighter_page_idpage = newplayerpage.idpage
                        newplayeronclub.group_page_idpage = page.idpage
                        newplayeronclub.group_idgroup = club.idgroup
                        db.session.add(newplayeronclub)
                        db.session.commit()
                        flash(newplayer.fighterName + " added to this club")
                    else:
                        if 'name' in request.form:
                            club.groupName = request.form['name']
                            db.session.add(club)
                            db.session.commit()

                        if 'email' in request.form:
                            club.groupEmail = request.form['email']
                            db.session.add(club)
                            db.session.commit()

                        if 'logo' in request.files:

                            if club.groupName == None:
                                flash('You must give this fighter a name before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            if club.groupcol == None:
                                flash('You must give this fighter a email before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            if club.groupcol == 'None':
                                flash('You must give this fighter a email before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            file = request.files['logo']
                            file.filename = club.groupName + "_" + club.groupcol + file.filename[-4::]
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                            for olderfile in os.listdir(app.config["UPLOAD_FOLDER"]):
                                if olderfile == club.groupLogo:
                                    if olderfile != file.filename:
                                        os.remove(app.config["UPLOAD_FOLDER"]+"/"+olderfile)
                            club.groupLogo = file.filename
                            db.session.add(club)
                            db.session.commit()

                        if 'nacionality' in request.form:
                            club.groupcol = request.form['nacionality']
                            db.session.add(club)
                            db.session.commit()

                    if 'delete' in request.form:
                        fpage = Page.query.filter_by(nome=request.form['delete']).first()
                        thisfighter = Fighter.query.filter_by(page_idpage=fpage.idpage).first()
                        hasgroup = Group_has_fighter.query.filter_by(group_idgroup=club.idgroup, fighter_idfighter=thisfighter.idfighter, group_has_fighter_entrance=request.form['Affiliation']).first()
                        db.session.delete(hasgroup)
                        db.session.add(thisfighter)
                        db.session.add(club)
                        db.session.commit()

                    if 'exiter' in request.form:
                        print(request.form)
                        fpage = Page.query.filter_by(nome=request.form['exiter']).first()
                        thisfighter = Fighter.query.filter_by(page_idpage=fpage.idpage).first()
                        hasgroup = Group_has_fighter.query.filter_by(group_idgroup=club.idgroup, fighter_idfighter=thisfighter.idfighter, group_has_fighter_entrance=request.form['Affiliation']).first()
                        hasgroup.group_has_fightercol_exit = request.form['exit']
                        db.session.add(hasgroup)
                        db.session.add(thisfighter)
                        db.session.add(club)
                        db.session.commit()

                    return redirect('/page/' + PageAddresi)

                if team:
                    newplayerpage = None
                    newplayer = None
                    newplayeronteam = Group_has_fighter()
                    newplayerrelation = None
                    if 'fighter' in request.form or 'capitain' in request.form or 'coach' in request.form or 'mercenary' in request.form:
                        if 'fighter' in request.form:
                            newplayerpage = Page.query.filter_by(nome=request.form['fighter']).first()
                            if newplayerpage == None:
                                flash("You must enter a fighter page name to invite to the team.")
                                return redirect('/page/' + PageAddresi)
                            newplayer = Fighter.query.filter_by(page_idpage=newplayerpage.idpage).first()
                            if Group_has_fighter.query.filter_by(fighter_idfighter=newplayer.idfighter,group_idgroup=team.idgroup,group_has_fighter_entrance=request.form['entrance']).first():
                                flash('This relation already existis')
                                return redirect('/page/' + PageAddresi)
                            newplayeronteam.relationtype = None
                            newplayerrelation = 'fighter'
                        if 'capitain' in request.form:
                            newplayerpage = Page.query.filter_by(nome=request.form['capitain']).first()
                            if newplayerpage == None:
                                flash("You must enter a fighter page name to invite to the team.")
                                return redirect('/page/' + PageAddresi)
                            newplayer = Fighter.query.filter_by(page_idpage=newplayerpage.idpage).first()
                            newplayeronteam.relationtype = 0
                            newplayerrelation = 'capitain'
                        if 'coach' in request.form:
                            newplayerpage = Page.query.filter_by(nome=request.form['coach']).first()
                            if newplayerpage == None:
                                flash("You must enter a fighter page name to invite to the team.")
                                return redirect('/page/' + PageAddresi)
                            newplayer = Fighter.query.filter_by(page_idpage=newplayerpage.idpage).first()
                            newplayeronteam.relationtype = 1
                            newplayerrelation = 'coach'
                        if 'mercenary' in request.form:
                            newplayerpage = Page.query.filter_by(nome=request.form['mercenary']).first()
                            if newplayerpage == None:
                                flash("You must enter a fighter page name to invite to the team.")
                                return redirect('/page/' + PageAddresi)
                            newplayer = Fighter.query.filter_by(page_idpage=newplayerpage.idpage).first()
                            newplayeronteam.relationtype = 2
                            newplayerrelation = 'mercenary'
                        if request.form['entrance'] == '':
                            flash("You must enter a affiliation date date to invite to the team.")
                            return redirect('/page/' + PageAddresi)
                        newplayeronteam.group_has_fighter_entrance = request.form['entrance']
                        newplayeronteam.fighter_idfighter = newplayer.idfighter
                        newplayeronteam.fighter_page_idpage = newplayerpage.idpage
                        newplayeronteam.group_page_idpage = page.idpage
                        newplayeronteam.group_idgroup = team.idgroup
                        db.session.add(newplayeronteam)
                        db.session.commit()
                        if newplayer.fighterName != None:
                            flash(newplayer.fighterName+" added to this team as "+newplayerrelation)
                        else:
                            flash("The fighter has been added to this team as " + newplayerrelation)

                    if 'delete' in request.form:
                        fpage = Page.query.filter_by(nome=request.form['delete']).first()
                        thisfighter = Fighter.query.filter_by(page_idpage=fpage.idpage).first()
                        hasgroup = Group_has_fighter.query.filter_by(group_idgroup=team.idgroup, fighter_idfighter=thisfighter.idfighter, group_has_fighter_entrance=request.form['Affiliation']).first()
                        db.session.delete(hasgroup)
                        db.session.add(thisfighter)
                        db.session.add(team)
                        db.session.commit()

                    if 'exiter' in request.form:
                        print(request.form)
                        fpage = Page.query.filter_by(nome=request.form['exiter']).first()
                        thisfighter = Fighter.query.filter_by(page_idpage=fpage.idpage).first()
                        hasgroup = Group_has_fighter.query.filter_by(group_idgroup=team.idgroup, fighter_idfighter=thisfighter.idfighter, group_has_fighter_entrance=request.form['Affiliation']).first()
                        hasgroup.group_has_fightercol_exit = request.form['exit']
                        db.session.add(hasgroup)
                        db.session.add(thisfighter)
                        db.session.add(team)
                        db.session.commit()

                    else:


                        if 'name' in request.form:
                            team.groupName = request.form['name']
                            db.session.add(team)
                            db.session.commit()

                        if 'email' in request.form:
                            team.groupEmail = request.form['email']
                            db.session.add(team)
                            db.session.commit()

                        if 'logo' in request.files:

                            if team.groupName == None:
                                flash('You must give this fighter a name before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            if team.groupcol == None:
                                flash('You must give this fighter a email before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            if team.groupcol == 'None':
                                flash('You must give this fighter a email before uploading a photo')
                                return redirect('/page/' + PageAddresi)
                            file = request.files['logo']
                            file.filename = team.groupName + "_" + team.groupcol + file.filename[-4::]
                            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                            for olderfile in os.listdir(app.config["UPLOAD_FOLDER"]):
                                if olderfile == team.groupLogo:
                                    if olderfile != file.filename:
                                        os.remove(app.config["UPLOAD_FOLDER"]+"/"+olderfile)
                            team.groupLogo = file.filename
                            db.session.add(team)
                            db.session.commit()

                        if 'nacionality' in request.form:
                            team.groupcol = request.form['nacionality']
                            db.session.add(team)
                            db.session.commit()


                    return redirect('/page/' + PageAddresi)

                if fighter:
                    #form = editorform()

                    if 'delete' in request.form:
                        thisgroup = Group.query.filter_by(groupName=request.form['delete']).first()
                        hasgroup = Group_has_fighter.query.filter_by(group_idgroup=thisgroup.idgroup,fighter_idfighter=fighter.idfighter,group_has_fighter_entrance=request.form['Affiliation']).first()
                        db.session.delete(hasgroup)
                        db.session.add(fighter)
                        db.session.add(thisgroup)
                        db.session.commit()

                    if 'name' in request.form:
                        fighter.fighterName = request.form['name']
                        db.session.add(fighter)
                        db.session.commit()

                    if 'email' in request.form:
                        fighter.fighterEmail = request.form['email']
                        db.session.add(fighter)
                        db.session.commit()

                    if 'gif' in request.files:

                        if fighter.fighterName == None:
                            flash('You must give this fighter a name before uploading a photo')
                            return redirect('/page/' + PageAddresi)
                        if fighter.fighterEmail == None:
                            flash('You must give this fighter a email before uploading a photo')
                            return redirect('/page/' + PageAddresi)
                        if fighter.fighterEmail == 'None':
                            flash('You must give this fighter a email before uploading a photo')
                            return redirect('/page/' + PageAddresi)
                        file = request.files['gif']
                        file.filename = fighter.fighterName + "_" + fighter.fighterNacionality + "_" + fighter.fighterEmail.split("@")[0] + "_" + PageAddresi + file.filename[-4::]
                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                        for olderfile in os.listdir(app.config["UPLOAD_FOLDER"]):
                            if olderfile == fighter.fighterGif:
                                if olderfile != file.filename:
                                    os.remove(app.config["UPLOAD_FOLDER"]+"/"+olderfile)
                        fighter.fighterGif = file.filename
                        db.session.add(fighter)
                        db.session.commit()


                    if 'Height' in request.form:
                        if request.form['Height'] != "":
                            if request.form['cm'] == 'inch':
                                heightcm = float(request.form['Height'])
                                heightcm = heightcm * 2.54
                                fighter.fighterHeight = heightcm
                            else:
                                fighter.fighterHeight = request.form['Height']
                            db.session.add(fighter)
                            db.session.commit()

                    if 'weight' in request.form:
                        if request.form['weight'] != "":
                            if request.form['kg'] == 'pound':
                                weightkg = float(request.form['weight'])
                                weightkg = weightkg*0.453592
                                fighter.fighterWeight = weightkg
                            else:
                                fighter.fighterWeight = request.form['weight']
                            db.session.add(fighter)
                            db.session.commit()

                    if 'age' in request.form:
                        if request.form['age'] != "":
                            fighter.fighterAge = request.form['age']
                            db.session.add(fighter)
                            db.session.commit()

                    if 'mainhand' in request.form:
                         fighter.fighterMainHand = request.form['mainhand']
                         db.session.add(fighter)
                         db.session.commit()

                    if 'nacionality' in request.form:
                         fighter.fighterNacionality = request.form['nacionality']
                         db.session.add(fighter)
                         db.session.commit()

                    if 'name' in request.form:
                         fighter.fighterName = request.form['name']
                         db.session.add(fighter)
                         db.session.commit()

                    if 'sex' in request.form:
                         fighter.fighterSex = request.form['sex']
                         db.session.add(fighter)
                         db.session.commit()


                    if 'header' in request.files:
                        if fighter.fighterName == None:
                            flash('You must give this fighter a name before uploading a header')
                            return redirect('/page/' + PageAddresi)
                        if fighter.fighterEmail == None:
                            flash('You must give this fighter a email before uploading a header')
                            return redirect('/page/' + PageAddresi)
                        if fighter.fighterEmail == 'None':
                            flash('You must give this fighter a email before uploading a header')
                            return redirect('/page/' + PageAddresi)
                        file = request.files['header']
                        file.filename = fighter.fighterName + "_" + fighter.fighterNacionality + "_" + PageAddresi +"_header"+ file.filename[-4::]
                        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
                        page.header = file.filename
                        db.session.add(page)
                        db.session.commit()



                    return redirect('/page/' + PageAddresi)

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
        if thispagehastype:
            # definig page content

            #typeObject = page.fetchPageTypeObject()
            #print(type(typeObject))


            if fighter:
                grouphas = Group_has_fighter.query.filter_by(fighter_idfighter=fighter.idfighter).all()
                tableteams = {'headers': ['Team name', 'Role', 'Logo', 'Affiliation date', 'Exit'],
                             'contents': []
                              }
                tableclubs = {'headers': ['Club name', 'Logo', 'Affiliation date', 'Exit'],
                              'contents': []
                              }
                for grouph in grouphas:
                    thisgroup = Group.query.filter_by(idgroup=grouph.group_idgroup).first()
                    if thisgroup.type == None:
                        role = None
                        if grouph.relationtype == None:
                            role = "Fighter"
                        if grouph.relationtype == 0:
                            role = "Capitain"
                        if grouph.relationtype == 1:
                            role = "Coach"
                        if grouph.relationtype == 2:
                            role = "Mercenary"
                        eachteam = Group.query.filter_by(idgroup=grouph.group_idgroup).first()
                        dic ={
                            'Team name': eachteam.groupName,
                            'Role': role,
                            'Logo': eachteam.groupLogo,
                            'Affiliation date': grouph.group_has_fighter_entrance,
                            'Exit': grouph.group_has_fightercol_exit,
                        }
                        tableteams['contents'].append(dic)

                    if thisgroup.type == 0:
                        eachteam = Group.query.filter_by(idgroup=grouph.group_idgroup).first()
                        dic = {
                            'Club name': eachteam.groupName,
                            'Logo': eachteam.groupLogo,
                            'Affiliation date': grouph.group_has_fighter_entrance,
                            'Exit': grouph.group_has_fightercol_exit,
                        }
                        tableclubs['contents'].append(dic)

                return render_template("beko/page/fighter.html", page=PageAddresi,
                                                                age=fighter.fighterAge,
                                                                email=fighter.fighterEmail,
                                                                gif=fighter.fighterGif,
                                                                weight=fighter.fighterWeight,
                                                                height=fighter.fighterHeight,
                                                                mainhand=fighter.fighterMainHand,
                                                                nacionality=fighter.fighterNacionality,
                                                                name=fighter.fighterName,
                                                                sex=fighter.fighterSex,
                                                                background=page.background,
                                                                header=page.header,
                                                                icone=page.icone,
                                                                relation=user,
                                                                table = tableteams,
                                                                tableclub=tableclubs




                                       )
            elif event:
                tablestages = {'headers': ['Stage Name','Fight','Date','Contestants'],
                             'contents': []
                              }
                allstages = Stage.query.filter_by(event_idevent=Event.idevent).all()
                for stage in allstages:
                    allstagefights = Fight.query.filter_by(stage_idstage=stage.idStage).all()

                    if len(allstagefights) == 0:
                        dic = {
                            'Stage Name': stage.stageName,
                            'Fight': None,
                            'Date': None,
                            'Contestants': None,
                        }

                        tablestages['contents'].append(dic)

                    else:
                        for eachfight in allstagefights:
                            fightgroups = Fight_has_group.query.filter_by(fight_idfight=eachfight.idfight).all()
                            allcontestants = ""
                            if len(fightgroups) == 0:
                                allcontestants = None
                            else:
                                i=0
                                for eachgroup in fightgroups:
                                    thegroup = Group.query.flter_by(idgroup = eachgroup.group_idgroup).first()
                                    if i == 0:
                                        allcontestants.append = thegroup.groupName
                                    else:
                                        allcontestants.append = (' X '+thegroup.groupName)
                                    i += 1



                            dic = {
                                'Stage Name': stage.stageName,
                                'Fight': eachfight.idfight,
                                'Date': eachfight.fightdate,
                                'Contestants': allcontestants ,
                            }
                            tablestages['contents'].append(dic)



                return render_template("beko/page/event.html", page=PageAddresi
                                                            ,tablestages=tablestages
                                                            ,relation=user
                                       )
            elif other:
                return render_template("beko/page/other.html", page=PageAddresi)
            elif club:
                grouphas = Group_has_fighter.query.filter_by(group_idgroup=club.idgroup).all()
                tablefighters = {'headers': ['fpage', 'Fighter name', 'Affiliation date', 'Exit'],
                                 'contents': []
                                 }
                for eachfighter in grouphas:

                    thisfighter = Fighter.query.filter_by(idfighter=eachfighter.fighter_idfighter).first()
                    fpage = Page.query.filter_by(idpage=thisfighter.page_idpage).first()

                    dic = {
                        'fpage': fpage.nome,
                        'Fighter name': str(thisfighter.fighterName),
                        'Affiliation date': eachfighter.group_has_fighter_entrance,
                        'Exit': eachfighter.group_has_fightercol_exit
                    }
                    tablefighters['contents'].append(dic)
                return render_template("beko/page/club.html", page=PageAddresi,
                                                              relation = user,
                                                              email=club.groupEmail,
                                                              logo=club.groupLogo,
                                                              header=page.header,
                                                              name=club.groupName,
                                                            nacionality=club.groupcol,
                                                            tablefighter=tablefighters,
                                       )
            elif team:
                grouphas = Group_has_fighter.query.filter_by(group_idgroup=team.idgroup).all()
                tablefighters = {'headers': ['fpage','Fighter name', 'Role', 'Affiliation date', 'Exit'],
                              'contents': []
                              }
                for eachfighter in grouphas:
                    role = None
                    if eachfighter.relationtype == None:
                        role = "Fighter"
                    if eachfighter.relationtype == 0:
                        role = "Capitain"
                    if eachfighter.relationtype == 1:
                        role = "Coach"
                    if eachfighter.relationtype == 2:
                        role = "Mercenary"

                    thisfighter = Fighter.query.filter_by(idfighter=eachfighter.fighter_idfighter).first()
                    fpage = Page.query.filter_by(idpage=thisfighter.page_idpage).first()

                    dic = {
                        'fpage' : fpage.nome,
                        'Fighter name' : thisfighter.fighterName,
                        'Role' : role,
                        'Affiliation date': eachfighter.group_has_fighter_entrance,
                        'Exit': eachfighter.group_has_fightercol_exit
                         }
                    tablefighters['contents'].append(dic)
                return render_template("beko/page/team.html", page=PageAddresi,
                                                              relation = user,
                                                              email=team.groupEmail,
                                                              logo=team.groupLogo,
                                                              header=page.header,
                                                              name=team.groupName,
                                                            nacionality=team.groupcol,
                                                            tablefighter=tablefighters,
                                       )
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
                    group = Group.query.filter_by(page_idpage=page.idpage).first()
                    if fighter is not None:
                        ghfs = Group_has_fighter.query.filter_by(fighter_idfighter=fighter.idfighter).all()
                        for ghf in ghfs:
                            db.session.delete(ghf)
                        db.session.delete(fighter)
                    if event is not None:
                        stages = Stage.query.filter_by(event_idevent=event.idevent).all()
                        for stage in stages:
                            stagefights = Fight.query.filter_by(stage_idstage=stage.idStage).all()
                            for fight in stagefights:
                                db.session.delete(fight)
                            db.session.delete(stage)
                        db.session.delete(event)
                    if other is not None:
                        db.session.delete(other)
                    if group is not None:
                        ghfs = Group_has_fighter.query.filter_by(group_idgroup=group.idgroup).all()
                        for ghf in ghfs:
                            db.session.delete(ghf)
                        db.session.delete(group)

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
