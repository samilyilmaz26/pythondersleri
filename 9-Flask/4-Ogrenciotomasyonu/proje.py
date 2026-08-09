from functools import wraps

from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3 
from passlib.hash import   sha256_crypt

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya gitmek için giriş yapmalısınız", "danger")
            return redirect(url_for("login"))
    return decorated_function 



app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/ogrenciler")
@login_required
def ogrenciler():
        con = sqlite3.connect("Ogrenci.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cmd = "select o.id, o.ad, o.soyad, b.bolumad from Ogrenci o inner join Bolum b on (o.Bolumid = b.id)"
        result = cursor.execute(cmd).fetchall()
        cursor.close()
        ogrenciler=[]
        for ogrenci in result:
            ogrenciler.append(dict(ogrenci))
        con.close()
        return render_template("ogrencilist.html", ogrenciler=ogrenciler)

@app.route("/ogrenci/ekle" , methods=["GET", "POST"])
@login_required
def ogrenci_ekle():
    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        bolumid = request.form.get("bolumid")
        
        con = sqlite3.connect("Ogrenci.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cmd = "insert into Ogrenci (ad,soyad,Bolumid) values (?,?,?)"
        cursor.execute(cmd, (ad, soyad, bolumid))
        con.commit()
        con.close()
        flash("Öğrenci Ekleme Başarılı", "success")
        return redirect(url_for("ogrenciler"))
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "select * from bolum"
    bolumler = cursor.execute(cmd).fetchall()
    cursor.close()
    con.close()
    return render_template("ogrenciekle.html", bolumler=bolumler)
    
@app.route("/ogrenci/sil/<int:id>")
@login_required
def ogrenci_sil(id):
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "delete from Ogrenci where id = ?"
    cursor.execute(cmd, (id,))
    con.commit()
    cursor.close()
    con.close()
    flash("Öğrenci Silme Başarılı", "success")
    return redirect(url_for("ogrenciler"))
@app.route("/ogrenci/guncelle/<int:id>", methods=["GET", "POST"])
@login_required
def ogrenci_guncelle(id):
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "select * from Ogrenci where id = ?"
    result = cursor.execute(cmd, (id,)).fetchone()
    ogrenci = dict(result)

    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        bolumid = request.form.get("bolumid")

        # if not ad or not soyad or not bolumid:
        #     flash("Tüm alanlar zorunludur", "danger")
        #     cursor.close()
        #     con.close()
        #     return render_template("ogrenciguncelle.html", ogrenci=ogrenci)

        cmd = "update Ogrenci set ad = ?, soyad = ?, Bolumid = ? where id = ?"
        cursor.execute(cmd, (ad, soyad, bolumid, id))
        con.commit()
        cursor.close()
        con.close()
        flash("Öğrenci Güncelleme Başarılı", "success")
        return redirect(url_for("ogrenciler"))

    cursor.close()
    con.close()
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "select * from bolum"
    result = cursor.execute(cmd).fetchall()
    bolumler = []
    for bolum in result:
        bolumler.append(dict(bolum))
     
    
    cursor.close()
    con.close()
     
    return render_template("ogrenciguncelle.html", ogrenci=ogrenci, bolumler=bolumler)

@app.route("/login" ,methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password_girilen = request.form.get("password")
        if not username or not password_girilen:
            flash("Tüm Alanları Doldurun ", "danger")
            return render_template("giris.html")
        con = sqlite3.connect("Ogrenci.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cmd = "select * from user where username = ?"
        result =  cursor.execute(cmd, (username,)).fetchone()
        user = dict(result)
        flash(str(user))
        if not  result :
            flash("Yanlış Kullanıcı veya şifre yanlış")
        esas_password = result[3]
        if sha256_crypt.verify(password_girilen, esas_password):
            session["logged_in"] = True
            session["username"] = username
            flash("Login Başarılı ...", "success")
            cursor.close()
            con.close
            return redirect(url_for("index"))
    return render_template("giris.html")
       
@app.route("/logout")
def logout():
     session.clear()
     flash("Çıkış Yaptınız","success")
     return redirect(url_for("index"))
@app.route("/degiskenler")
def degiskenler():
        isim = "Ali"
        yas = 25
        user = {"isim":"Ali" , "yas":25}
        userlist = [{"isim":"Ali" , "yas":25},
                    {"isim":"Veli" , "yas":30}, 
                    {"isim":"Ayşe" , "yas":20}]
        return render_template("degiskenler.html" ,isim = isim, yas = yas, user = user, userlist = userlist)

@app.route('/register' , methods = ["GET","POST"])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        accept_tos = request.form.get("accept_tos")
        if not username or not email or not password or not confirm or not accept_tos:
            flash("Tüm Alanlar Doldurulmalı " , "danger")
            return render_template("kayit.html")
        elif password != confirm:
            flash("Şifreler uyuşmuyor"   ,  "danger")
        hash_password = sha256_crypt.encrypt(password)
        con = sqlite3.connect("Ogrenci.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()

        cmd = "insert into User (username,password,email ) values (? ,? ,?) "
        cursor.execute(cmd , (username,hash_password,email))
        con.commit()
        con.close()
        flash("Sisteme üye kaydı başarılı ","success")
        return redirect(url_for("index"))
    return render_template("kayit.html")
@app.route("/bolumler")
@login_required
def bolumler():
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "select * from bolum"
    result = cursor.execute(cmd).fetchall()
    cursor.close()

   # bolumler = [dict(bolum) for bolum in result]
    bolumler=[]
    for bolum in result:
        bolumler.append(dict(bolum))
    con.close()

    return render_template("bolumlist.html", bolumler=bolumler)

@app.route("/bolum/ekle" , methods=["GET", "POST"])
@login_required
def bolum_ekle():
    if request.method == "POST":
        bolumad = request.form.get("bolumad")
        
        con = sqlite3.connect("Ogrenci.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cmd = "insert into bolum (bolumad) values (?)"
        cursor.execute(cmd, (bolumad,))
        con.commit()
        con.close()
        flash("Bölüm Ekleme Başarılı", "success")
        return redirect(url_for("bolumler"))
    return render_template("bolumekle.html")
@app.route("/bolum/guncelle/<int:id>", methods=["GET", "POST"])

@login_required
def bolum_guncelle(id):
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "select * from bolum where id = ?"
    result = cursor.execute(cmd, (id,)).fetchone()

    if not result:
        cursor.close()
        con.close()
        flash("Bölüm bulunamadı", "danger")
        return redirect(url_for("bolumler"))

    bolum = dict(result)

    if request.method == "POST":
        bolumad = request.form.get("bolumad")
        if not bolumad:
            flash("Bölüm adı boş olamaz", "danger")
            cursor.close()
            con.close()
            return render_template("bolumguncelle.html", bolum=bolum)

        cmd = "update bolum set bolumad = ? where id = ?"
        cursor.execute(cmd, (bolumad, id))
        con.commit()
        cursor.close()
        con.close()
        flash("Bölüm Güncelleme Başarılı", "success")
        return redirect(url_for("bolumler"))

    cursor.close()
    con.close()
    return render_template("bolumguncelle.html", bolum=bolum)

@app.route("/bolum/sil/<int:id>" )
@login_required
def bolum_sil(id):
    con = sqlite3.connect("Ogrenci.db")
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cmd = "delete  from bolum where id = ?"
    cursor.execute(cmd, (id,))
    con.commit()
    cursor.close()
    con.close()
    flash("Bölüm Silme Başarılı", "success")
    return redirect(url_for("bolumler"))

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)