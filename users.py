import os
import secrets
from db import db
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
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
            session["csrf_token"] = secrets.token_hex(16)

            return redirect("/")
        else:
            return render_template("login.html", loginError = True)

def logout():
    if "username" in session.keys():
        del session["username"]
    return redirect("/login")

def register(username, password):
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

def user_id():
    return session.get("user_id",0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)