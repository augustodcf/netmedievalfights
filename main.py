from flask import Flask, escape, request, url_for, render_template, abort, flash, redirect
import json
from controllers import blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, SelectFieldBase, PasswordField
from wtforms.validators import DataRequired
from flask_debug import Debug
from flask_bootstrap import Bootstrap



app = Flask(__name__)

Bootstrap(app)
Debug(app)
app.secret_key = b"""_5#y2L"F4Q8z\n\xec]/"""
app.config["SQLALCHEMY_DATABASE_URI"] = """mysql://root:6=2Cxl{3t6}g[pD@localhost/medievalfights"""
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


User_has_page = db.Table('user_has_page',
    db.Column('user_id', db.Integer, db.ForeignKey('user.idUser'), primary_key=True),
    db.Column('page_idpage', db.Integer, db.ForeignKey('page.idpage'), primary_key=True),
    db.Column('user_has_page_relationtype', db.String(1), unique=False, nullable=True),
)

class User(db.Model):
    idUser = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(45), unique=True, nullable=True)
    email = db.Column(db.String(45), unique=False, nullable=True)
    active = db.Column(db.Boolean, unique=False, nullable=True, default = True)
    authenticated = False
    pages = db.relationship('Page', secondary=User_has_page, lazy='subquery', backref=db.backref('user', lazy=True))

    def is_authenticated (self):
        return self.authenticated
    def is_active (self):
        return self.active
    def is_anonymous (self):
        return False
    def get_id(self):
        return self.idUser

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(idUser= user_id) .first()
    print(user)
    return user



class Page(db.Model):
    idpage         = db.Column(db.Integer, primary_key=True)
    nome     = db.Column(db.String(45), unique=True, nullable=False)
    icone      = db.Column(db.String(45), unique=True, nullable=True)
    header     = db.Column(db.String(45), unique=False, nullable=True)
    background = db.Column(db.String(45), unique=False, nullable=True)
  
    #User_idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'),
    #nullable=False)
    #User = db.relationship('User',
    #    backref=db.backref('user', lazy=True))

class Fighter(db.Model):
    idfighter          = db.Column(db.Integer, primary_key=True)
    fighterName        = db.Column(db.String(255), unique=True, nullable=False)
    fighterAge         = db.Column(db.Integer(), unique=False, nullable=False)
    fighterWeight      = db.Column(db.Integer(), unique=False, nullable=False)
    fighterHeight      = db.Column(db.Integer(), unique=False, nullable=False)
    fighterMainHand    = db.Column(db.String(1), unique=False, nullable=False)
    fighterEmail       = db.Column(db.String(255), unique=False, nullable=False)
    fighterGif         = db.Column(db.String(45), unique=True, nullable=True)
    fighterSex         = db.Column(db.String(1), unique=False, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username

class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    psw = PasswordField('psw', validators=[DataRequired()])
    repassword = PasswordField('repassword', validators=[DataRequired()])
    #Agree = SelectFieldBase('', validators=[DataRequired])
    Submit: SubmitField = SubmitField('Submit')

class Addpage(FlaskForm):
    pagename = StringField('pagename', validators=[DataRequired()])
    Submit: SubmitField = SubmitField('Submit')

db.create_all()



#club = {
#    "rosadeferro" : {
#
#    }
#}

#cliente = {
#    0 : {
#        "nome": "arbusto",
#        "sobrenome": "gustavo",
#        "idade": 10,
#        "telefone": 22441000
#    }
#}

#@app.route('/')#default = GET
#def hello():
#    name = request.args.get("name", "World")
#    return f'Hello, {escape(name)}!'

#@app.route('/nome/<meunome>')
#def name(meunome):
#    return 'Hello, %s!' % meunome, 200

#@app.route('/cliente/<int:id>', methods=["GET","POST"])
#def clienteAPI(id=-1):
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
    return render_template ("beko/index.html")


@app.route("/page/<string:PageAddresi>", methods = ["GET"])
def route_page(PageAddresi):
    if request.method == "GET":
        #q = Page.query.all()
        #i = 0
        #strings = ["tornadoferreira", "stevejobs"]
        #for page in q:
        #    print(page)
        #    page.PageAddres = strings[i]
        #    i+=1
        #    db.session.add(page)
        #    db.session.commit()
        page = Page.query.filter_by(PageAddres= PageAddresi) .all()
        print (PageAddresi)
        if page:
            return render_template("beko/fighter.html")
        else:
            return "", 401


@app.route("/testelog")
@login_required
def testelog():
    return "Hello, "+current_user.username+"!",200

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MyForm()
    #print (form.validate_on_submit())
    if form.validate_on_submit():
        if form.psw.data != form.repassword.data:
            flash ("The passwords do not match.")
            return redirect(url_for('register'))

        user = User(username = form.username.data, password = form.psw.data, email = form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(request.args.get("next") or url_for('index'))
    return render_template('/beko/userregisterwtf.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    #form = LoginForm()
    #if form.validate_on_submit():
    if request.method == "POST":
        
        user = User.query.filter_by(userName = request.form['username']).first()
        if user is not None and request.form['password'] == user.password:
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            #if not is_safe_url(next):
            #    return abort(400)

            return redirect(next or url_for('index'))
        return "Login Failed!"
    
    #user = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    #db.session.add(user)
    #db.session.commit()
    return render_template('/beko/login.html') #, form=form))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You are now logged out."

@app.route("/pageadm", methods=['GET', 'POST'])
@login_required
def pageadm():
    table = {'headers': ['Name', 'Relationship', 'Share'],
             'contents': []
             }
    for page in current_user.pages:
        relation = db.select([User_has_page]).where(User_has_page.c.page_idpage == page.idpage).where(User_has_page.c.user_id == current_user.idUser)
        relation = relation.compile(compile_kwargs={"literal_binds": True})

        dic = {'Name': page.nome,
                'Relationship': relation.user_has_page_relationtype,
                'Share': 'Preencher no futuro' ,
                }
        table['contents'].append(dic)
    print(paginasdouser)

    # User_has_page.query.filter_by(page_idpage = page.idpage, user_id = current_user.idUser).first().user_has_page_relationtype,

    return render_template('beko/userhaspages.html',table = table)

@app.route("/pageregister", methods=['GET','POST'])
@login_required
def pageregister():
    pageform = Addpage()
    if pageform.validate_on_submit():
        page = Page(nome = pageform.pagename.data)
        db.session.add(page)
        current_user.pages.append(page)
        db.session.add(current_user)
        db.session.commit()


    return render_template('/beko/userregisterpage.html', form=pageform)

#def iniciarbanco():
    #user1 = User(UserName="arbusto", Password="werwer", Email="jenkins@leroy.com")
    #db.session.add(user1)

    #user2 = User(UserName="tony", Password="123123", Email="jenkins@leroytcs.com")
    #db.session.add(user2)

    #fighter = Fighter(
        #FighterName        = "Tornado Ferreira",
        #FighterAge         = 1988,
        #FighterWeight      = 90,
        #FighterHeight      = 175,
        #FighterMainHand    = "R",
        #FighterEmail       = "johnbiritones@gmail.com",
        #FighterGif         = None,
        #FighterSex         = "M",
    #)
    #db.session.add(fighter)

    #page = Page(
        #PageAddres     = "tferreira",
        #PagePhoto      = None,
        #PageHeader     = None,
        #PageBackground = None,
    #)
    #db.session.add(page)

    #user_page = User_has_page (
        #User_idUser            = 1,
        #Page_idPage            = page.idPage,
        #Page_User_idUser       = None,
        #Page_Club_idClub       = None,
        #Page_Fighter_idFighter = fighter.idFighter,
        #user_has_PageRelation  = "C",
    #)
    #db.session.add(user_page)

    #db.session.commit()

#iniciarbanco()

app.run(debug=True)

