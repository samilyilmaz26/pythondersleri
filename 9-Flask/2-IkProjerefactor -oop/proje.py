from flask import Flask , flash, render_template, redirect, url_for, request,session
import sqlite3
from passlib.hash import   sha256_crypt
from datetime import date
from functools import wraps
from modul.sehirmodul import sehirRepository

app = Flask(__name__)
app.secret_key = "secret"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya gitmek için giriş yapmalısınız", "danger")
            return redirect(url_for("login"))
    return decorated_function 
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/register' , methods = ["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        accept_tos = request.form.get("accept_tos")

        if not email or not email or not password or not confirm:
            flash("Lütfen tüm alanları doldurun", "danger")
            return render_template("register.html")

        if password != confirm:
            flash("Parolalar eşleşmiyor", "danger")
            return render_template("register.html")

        if not accept_tos:
            flash("Kullanım şartlarını kabul etmelisiniz", "danger")
            return render_template("register.html")

        hashed_password = sha256_crypt.encrypt(password)
        con = sqlite3.connect("Banka.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute('insert into user (email,email,password) values(? , ? ,?)', (email,email,hashed_password))
        con.commit()
        cursor.close()
        flash("Kayıt İşlemi Başarılı.." ,"success")
        return redirect(url_for("index"))

    return render_template("register.html")
@app.route('/login' , methods = ["GET" ,"POST"] )
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password_entered = request.form.get("password")
        flash(email)
        flash(password_entered)
        if not email or not password_entered:
            flash("Kullanıcı adı ve şifre giriniz", "danger")
            return redirect(url_for("login"))

        con = sqlite3.connect("Banka.db")
        cursor = con.cursor()
        con.row_factory = sqlite3.Row
        sorgu = 'select * from user where email = ?'
        result = cursor.execute(sorgu, (email,)).fetchone()
        cursor.close()

        if result:
            password_real = result[2]
            if sha256_crypt.verify(password_entered, password_real):
                session["logged_in"] = True
                session["email"] = email
                flash("Login Başarılı ...", "success")
                return redirect(url_for("index"))
            else:
                flash("yanlış şifre ", "danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle Bir Kullanıcı Yok....", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")
@app.route('/logout' , methods = ["GET" ,"POST"] )
def logout():
    session.clear()
    return redirect(url_for("index"))
@login_required
@app.route('/cities/list')
def list():
    repo = sehirRepository()
    sehirler = repo.get_all()  # Contains a list of PersonelModel instances
    for s in sehirler:
        flash(s.ad)
    return render_template("sehir/list.html", sehirler=sehirler)

@app.route('/cities/edit/<string:id>',methods = ["GET","POST"])
@login_required
def edit(id):
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    if request.method == "GET":
        sorgu = 'select * from city where id = ?'
        city = cursor.execute(sorgu,(id,)).fetchone()
        return render_template("cities/edit.html", city=city)

    name = request.form.get("name")
    if not name :
        flash("Lütfen tüm alanları doldurun", "danger")
        city = cursor.execute('select * from city where id = ?', (id,)).fetchone()
        return render_template("cities/edit.html", city=city)

    sorgu = 'update city set name = ?  where id = ?'
    cursor.execute(sorgu, (name, id))
    con.commit()
    flash("Güncelleme Başarılı", "success")
    return redirect(url_for("list"))
@app.route('/cities/delete/<string:id>',methods = ["GET","POST"])
@login_required
def delete(id):
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    
    if request.method == "GET":
        sorgu = 'select * from city where id = ?'
        city = cursor.execute(sorgu,(id,)).fetchone()
 
        return render_template("cities/delete.html", city=city)

    sorgu = 'delete from city where id = ?'
    cursor.execute(sorgu, (id,))
    con.commit()
    flash("Silme Başarılı", "success")
    return redirect(url_for("list"))
@app.route('/cities/add',methods = ["GET","POST"])
@login_required
def add():
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row 
    cursor = con.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        if not name : 
            flash("Lütfen tüm alanları doldurun", "danger")

        sorgu = 'insert into city (name) values (?)'
        cursor.execute(sorgu, (name, ))
        con.commit()
        flash("Yeni kayıt Eklendi", "success")
        return redirect(url_for("list"))

    return render_template("cities/add.html")
@app.route('/personel/list')
@login_required
def perlist():
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    
    sorgu = 'select * from personel'
    personel = cursor.execute(sorgu).fetchall()
    return render_template("personel/list.html" ,personel = personel)  

@app.route('/personel/add',methods = ["GET","POST"])
@login_required
def peradd():
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    sorgu = 'select id, name  from city'
    cities=  cursor.execute(sorgu).fetchall()
   
    
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        salary = request.form.get("salary")
        birthdate = request.form.get("birthdate")
        cityid = request.form.get("cityid")

        if not all([name, surname, salary, birthdate, cityid]):
            flash(name +surname +  salary +  birthdate + cityid)
            flash("Lütfen tüm alanları doldurun", "danger")
            return render_template("personel/add.html", cities=cities)

        sorgu = 'insert into personel (name, surname, salary, birthdate, cityid) values (?, ?, ?, ?, ?)'
        cursor.execute(sorgu, (name, surname, float(salary), birthdate, cityid))
        con.commit()
        flash("Yeni kayıt Eklendi", "success")
        return redirect(url_for("perlist"))
    return render_template("personel/add.html", cities=cities) 
@app.route('/personel/edit/<string:id>',methods = ["GET","POST"])
@login_required
def peredit(id):
    
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    sorgu = 'select id, name from city'
    cities = cursor.execute(sorgu).fetchall()
        
    if request.method == "GET":
        sorgu = 'select * from personel where id = ?'
        personel = cursor.execute(sorgu, (id,)).fetchone()
         

        return render_template("personel/edit.html", personel=personel, cities=cities)
         
    elif request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        salary = request.form.get("salary")
        cityid = int(request.form.get("cityid"))
        birthdate = request.form.get("birthdate")
        if not all([name, surname, salary, birthdate]):
            flash("Lütfen tüm alanları doldurun", "danger")
            return render_template("personel/edit.html", cities=cities, birthdate=birthdate, cityid=cityid)
        sorgu = 'update personel set name = ?, surname = ?, salary = ?, birthdate = ?, cityid = ? where id = ?'
        cursor.execute(sorgu, (name, surname, float(salary), birthdate, cityid, id))
        con.commit()
        flash("Güncelleme Başarılı", "success")
        return redirect(url_for("perlist"))
    
@app.route('/personel/delete/<string:id>')
@login_required
def perdelete(id):
    con = sqlite3.connect("Banka.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    sorgu = 'delete from personel where id = ?'
    cursor.execute(sorgu, (id,))
    con.commit()
    flash("Silme Başarılı " ,"success")
    return redirect(url_for("perlist"))
 
if __name__ =="__main__":
    #db.create_all()
    app.run(debug = True)  



 


