from app import app
from flask import render_template
from crypt import methods
from itertools import product
from pickle import TRUE
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

@app.route("/")
def index():
    if "username" not in session.keys():
        return redirect("/login")
    sql = "SELECT  id, category, product, price FROM costs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":session["userid"]})
    costs = result.fetchall()
    return render_template("index.html", session=session, costs=costs)

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
            session["userid"] = user.id
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

@app.route("/new", methods=["GET", "POST"])
def new():
    if "username" not in session.keys():
        return redirect("/login")
    if request.method == "GET":
        return render_template("new.html")
    category = request.form["category"]
    product = request.form["product"]
    price = int(request.form["price"])
    sql = "INSERT INTO costs (category, product, price, userid) VALUES (:category, :product, :price, :userid)"
    db.session.execute(sql, {"category":category, "product":product, "price":price, "userid":session["userid"]})
    db.session.commit()
    return redirect("/")
