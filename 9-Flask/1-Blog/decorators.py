from flask import  Flask ,request, redirect, url_for,session,flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya gitmek için giriş yapmalısınız", "danger")
            return redirect(url_for("login"))
    return decorated_function 

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            role = str(session["role"])
        except :
            role = " "
        if  role == "admin":
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya gitmek admin olmalısınız ", "danger")
            return redirect(url_for("login"))
    return decorated_function 
 
 