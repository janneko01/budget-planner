from os import abort
from app import app
from flask import render_template
from crypt import methods
from itertools import product
from pickle import TRUE
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import users

from db import db

@app.route("/")
def index():
    if "username" not in session.keys():
        return redirect("/login")
    sql = "SELECT  id, category, product, price FROM costs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":session["userid"]})
    costs = result.fetchall()

    sql_categories = "SELECT category, sum(price) FROM costs WHERE userid=:userid GROUP BY category"
    result_categories = db.session.execute(sql_categories, {"userid":session["userid"]})
    costsByCategories = result_categories.fetchall()
    print(costsByCategories)
    return render_template("index.html", session=session, costs=costs, costsByCategories=costsByCategories)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
    if "username" not in session.keys():
        return redirect("/login")
    if request.method == "GET":
        return render_template("new.html", session=session)
    users.check_csrf()
    category = request.form["category"]
    product = request.form["product"]
    price = int(request.form["price"])
    eventDate = request.form["date"]
    sql = "INSERT INTO costs (category, product, price, eventDate, userid) VALUES (:category, :product, :price, :eventDate, :userid)"
    db.session.execute(sql, {"category":category, "product":product, "price":price, "eventDate":eventDate, "userid":session["userid"]})
    db.session.commit()
    return redirect("/")

@app.route("/income", methods=["GET", "POST"])
def income():
    if "username" not in session.keys():
        return redirect("/login")
    if request.method == "GET":
        return render_template("income.html", session=session)
    users.check_csrf()
    source = request.form["source"]
    income = request.form["income"]
    eventDate = request.form["date"]
    sql = "INSERT INTO income (source, income, eventDate, userid) VALUES (:source, :income, :eventDate, :userid)"
    db.session.execute(sql, {"source":source, "income":income, "eventDate":eventDate, "userid":session["userid"]})
    db.session.commit()
    return redirect("/")