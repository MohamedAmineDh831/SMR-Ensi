from flask import Flask,redirect,session,request
import os
import time
import firebase
import random
import threading
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, ValidationError
from flask import Flask, render_template, url_for
from pyrebase import pyrebase

app = Flask(__name__)


SESSION_TYPE = 'redis'
app.config["SECRET_KEY"]=os.urandom(24)

dash = None

#app.config['SECRET_KEY'] = 'secret!'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    def validate_usr(self):
        if self.username.data != "Mohamed" :
            raise ValidationError('Username is Incorrect')



class MyForm(LoginForm):
    email = StringField('Email adress', validators=[InputRequired('erreur email')])
    username = StringField('Username', validators=[InputRequired(message='errrrrrrrrrrr')])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    Tel = StringField('Tel', validators=[InputRequired()])
    about_me = TextAreaField('About Me')


class ReunionForm(FlaskForm):
    nom = StringField('name')
    nom_formateur = StringField("Formator", validators=[InputRequired("errur")])
    heure= IntegerField('hours', validators=[InputRequired(message='errrrrrrrrrrr')])
    date = StringField('date', validators=[InputRequired()])
    Duree = IntegerField('Duree', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    description = TextAreaField('Description')




def Courbe():
    i=0
    while (1):
        i += 1
        T = random.randint(30, 32)
        H = random.randint(1, 100)/100
        L = random.randint(0, 5)
        time.sleep(4)
        firebaseConfig = {
            "apiKey": "AIzaSyDzMn2-97STkm94Rex_4kyt0Vjj8wfGTOY",
            "authDomain": "powerful-loader-298710.firebaseapp.com",
            "databaseURL": "https://powerful-loader-298710-default-rtdb.firebaseio.com/",
            "storageBucket": "powerful-loader-298710.appspot.com",
        }
        firebase = pyrebase.initialize_app(firebaseConfig)
        database = firebase.database()

        database.child("cities").child("cities").update({"cp": T, "altitude": H, "lum": L})



@app.route('/user_register/<idp>', methods=['GET', 'POST'])
def user_register(idp):
    form = MyForm()
    t = len(firebase.database.child("user").get().val())
    if form.validate_on_submit():
        firebase.database.child("user").child(form.username.data).set(
            { "id" : t,
              "firstname": form.first_name.data,
              "lastname": form.last_name.data,
             "email": form.email.data,
              "password": form.password.data
              })
    if idp == 0:
        values = firebase.child("Reunion").child(session["ReunionId"]).get()
        val = values.val()
        invite = val["ivités"]
        invite = invite+str(t)
        print(invite)
        firebase.database.child("Reunion").child(session["ReunionId"]).update(
            {"invités": invite})
    return render_template('user_register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        values = firebase.database.child('user').child(username).get()
        val=values.val()
        v2=val['password']

        if v2 == password:
            session['Login'] = username
            return "authentification valide"
        else:
            return "no"
    return render_template('login.html', form=form)



@app.route('/room', methods=["GET", "POST"])
def room():
    L = []
    values = firebase.database.child("Room").get()
    val = values.val()
    if request.method == "POST":
        for i in range(len(val)):
            print(request.form["Room"])
            if request.form["Room"] == "Room"+str(i):
                print("if"+str(i))
                session["RoomId"]="Room"+str(i)
                return redirect(url_for("room2"))
    for v, i in enumerate(val):
        L.append(val["Room"+str(v)])
    return render_template('room.html', L=L)


@app.route('/room2', methods=["GET", "POST"])
def room2():
    firebase.database.child("Reunion").child("reunion2").update(
        {"nom": session["nom"],
         "date": session["date"],
         "heure": session["heure"],
         "Duree": session["Duree"],
         "roomid": session["RoomId"],
         "adresse": session["adresse"],
         "city": session["city"]
         })
    return render_template("Home.html")



@app.route('/',methods=['GET', 'POST'])
def Home():
    user = None
    if 'Login' in session:
        user = session["Login"]
    L = []
    values = firebase.database.child("Reunion").get()
    val = values.val()
    values2 = firebase.database.child("user").get()
    val2 = values2.val()
    UserId = []
    for v, i in enumerate(val):
        nomformateur = val["reunion" + str(v)]["NomFormateur"]
        for j in val2:
            if val2[j]["lastname"] == nomformateur:
                UserId.append(val2[j]["id"])
        L.append(val["reunion" + str(v)])
        taille = len(L)
    if request.method == "POST" :
        for i in range(len(val)) :
            if request.form["Reunion"] == "reunion"+str(i) :
                session["ReunionId"]="reunion"+str(i)
                return redirect(url_for("login"))
    return  render_template('Home.html', taille=taille, L=L, UserId=UserId, login= user)



@app.route('/addreunion',methods=['GET', 'POST'])
def addreunion():
   form = ReunionForm()
   if form.validate_on_submit():
       session["nom"] = form.nom.data
       session["date"] = form.date.data
       session["heure"] = form.heure.data
       session["Duree"] = form.Duree.data
       session["adresse"] = form.address.data
       session["city"] = form.city.data
       return redirect(url_for("room"))
   return render_template('addreunion.html', form=form)



@app.route('/notifications')
def notification():
    return render_template('notifications.html')


@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')


@app.route('/dashboard')
def dashboard():
    thread = threading.Thread(target=Courbe)
    thread.daemon = True  # Daemonize
    thread.start()
    session["dash"] = 'ok'
    return render_template('dashboard.html')

def room_caracteristics():
    return "hello world"


if __name__ == '__main__':
    app.run(threaded=True, debug=True)

