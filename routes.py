from os import abort
from app import app
from flask import flash, render_template
from crypt import methods
from itertools import product
from pickle import TRUE
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import users
import costs
import incomes

from db import db

@app.route("/")
def index():
    if "username" not in session.keys():
        return redirect("/login")
    sql = "SELECT  id, category, product, price FROM costs WHERE userid=:userid"
    result = db.session.execute(sql, {"userid":session["userid"]})
    costs1 = result.fetchall()

    costsWithCategories = costs.get_costs_with_categories(session["userid"])
    allcosts = costs.get_costs(session["userid"])
    monthlyCosts = costs.get_costs_by_month(session["userid"])
    costsByMonth = costs.get_costs_by_month(session["userid"])

    sql_categories = "SELECT category, sum(price) FROM costs WHERE userid=:userid GROUP BY category"
    result_categories = db.session.execute(sql_categories, {"userid":session["userid"]})
    costsByCategories = result_categories.fetchall()
    print(costsByCategories)
    return render_template("index.html", session=session, costs=costs1, costsByCategories=costsByCategories, costsByMonth=costsByMonth)

@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session.keys():
        return redirect("/")
    
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        loggedInSuccessfully = users.login(username, password)
        if loggedInSuccessfully:
            return redirect("/")
        error = "Väärä käyttäjätunnus tai salasana"        
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session.keys():
        return redirect("/")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            error = "Rekisteröinti ei onnistunut, koska käyttäjätunnus (min. 5 merkkiä) tai salasana (min. 8 merkkiä) on liian lyhyt tai käyttäjätunnus on jo olemassa."
    return render_template("register.html", error = error)



@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/costs", methods=["GET", "POST"])
def new():
    if "username" not in session.keys():
        return redirect("/login")
    if request.method == "GET":
        monthlyCosts = costs.get_this_month_costs(session["userid"])
        print(monthlyCosts)
        return render_template("costs.html", session=session, monthlyCosts=monthlyCosts)
    users.check_csrf()
    category = request.form["category"]
    product = request.form["product"]
    price = request.form["price"]
    eventDate = request.form["date"]
    if len(product) > 20 or len(product) < 3:
        flash("Tuotetta ei voitu lisätä. Tuotteen nimi on liian pitkä tai liian lyhyt.")
        return render_template("costs.html")
    if not price.isnumeric() or len(price) > 7:
        flash("Tuotetta ei voitu lisätä. Tarkista hinta.")
        return render_template("costs.html")
    sql = "INSERT INTO costs (category, product, price, eventDate, userid) VALUES (:category, :product, :price, :eventDate, :userid)"
    db.session.execute(sql, {"category":category, "product":product, "price":price, "eventDate":eventDate, "userid":session["userid"]})
    db.session.commit()
    return redirect("/costs")

@app.route("/income", methods=["GET", "POST"])
def income():
    if "username" not in session.keys():
        return redirect("/login")
    if request.method == "GET":
        monthlyIncome = incomes.get_incomes(session["userid"])
        return render_template("income.html", session=session, monthlyIncome=monthlyIncome)
    users.check_csrf()
    source = request.form["source"]
    amount = request.form["income"]
    eventDate = request.form["date"]
    if len(source) > 20 or len(source) < 3:
        flash("Tuloa ei voitu lisätä. Tulon lähde liian pitkä tai liian lyhyt.")
        return render_template("income.html")
    if not amount.isnumeric() or len(amount) > 7:
        flash("Tuloa ei voitu lisätä. Tarkista tulon määrä.")
        return render_template("income.html")
    sql = "INSERT INTO income (source, income, eventDate, userid) VALUES (:source, :income, :eventDate, :userid)"
    db.session.execute(sql, {"source":source, "income":amount, "eventDate":eventDate, "userid":session["userid"]})
    db.session.commit()
    return redirect("/income")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" not in session.keys():
        return redirect("/login")
    sql = "SELECT targetbudget FROM usersettings WHERE userid=:userid"
    budget = db.session.execute(sql, {"userid":session["userid"]}).fetchone()
    if budget:
        budget = budget[0]
    else:
        budget = ""

    if request.method == "GET":
        return render_template("settings.html", session=session, budget=budget)
    users.check_csrf()
    targetBudget = request.form["targetbudget"]
    if not targetBudget.isnumeric() or len(targetBudget) > 7:
        flash("Budjetin tulee olla kokonaisluku")
        return render_template("settings.html")
    targetBudget = int(targetBudget)    
    if budget:
        sql = "UPDATE usersettings SET targetbudget=:targetbudget WHERE userid=:userid"
    else:
        sql = "INSERT INTO usersettings (targetbudget, userid) VALUES (:targetbudget, :userid)"
    db.session.execute(sql, {"targetbudget":targetBudget, "userid":session["userid"]})
    db.session.commit()
    flash("Budjettitavoite päivitetty")
    return redirect("/settings")
