from repo.connection import opendb 
from flask import session, flash, redirect, url_for
from functools import wraps 

@opendb
def bul(con, id):
    cursor = con.cursor()
    cmd = "select * from user where id = ?"
    result = cursor.execute(cmd, (id,)).fetchone()
    if result:
        return dict(result)
    else:
        return None

@opendb
def login(con, username):
    cursor = con.cursor()
    cmd = "select * from user where username = ?"
    result = cursor.execute(cmd, (username,)).fetchone()
    if result:
        return dict(result)
    else:
        return None

def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız", "success")
    return redirect(url_for("index"))

@opendb
def kayitol (con, username, password):
    cursor = con.cursor()
    cmd = "insert into user (username, password) values (?,?)"
    cursor.execute(cmd, (username, password))
    con.commit()

@opendb
def verifypassword(con, username, password):
    cursor = con.cursor()
    cmd = "select * from user where username = ?"
    result = cursor.execute(cmd, (username,)).fetchone()
    if result:
        stored_password = result["password"]
        return stored_password == password
    else:
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya gitmek için giriş yapmalısınız", "danger")
            return redirect(url_for("login"))
    return decorated_function
