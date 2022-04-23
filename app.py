
from crypt import methods
from pickle import TRUE
from unittest import result
from flask import Flask, redirect, request, session
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:heppa@localhost:5432/postgres"
db = SQLAlchemy(app)
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    if "username" not in session.keys():
        return redirect("/login")
    sql = "SELECT  id, income, usedIncome FROM budget"
    #result = db.session.execute(sql)
    return render_template("index.html", session=session)

@app.route("/login",methods=["GET", "POST"])
def login():
    if "username" in session.keys():
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("login.html", loginError = True)
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", loginError = True)

@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session.keys():
        return redirect("/")
    if request.method == "GET":
        return render_template("register.html")
    
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/login")

@app.route("/logout")
def logout():
    if "username" in session.keys():
        del session["username"]
    return redirect("/login")

@app.route("/new")
def new():

    return render_template("add.html")
