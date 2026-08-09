from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3 
from passlib.hash import   sha256_crypt

from repo import bolumrepo as br
from repo import ogrencirepo as op
from repo.userrepo import login_required
import repo.userrepo as up

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
    ogrenciler = op.liste()
    return render_template("ogrencilist.html", ogrenciler=ogrenciler)

@app.route("/ogrenci/ekle" , methods=["GET", "POST"])
@login_required
def ogrenci_ekle():
    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        bolumid = request.form.get("bolumid")
        op.ekle(ad, soyad, bolumid)
        flash("Öğrenci Ekleme Başarılı", "success")
        return redirect(url_for("ogrenciler"))
    bolumler = br.liste()
    return render_template("ogrenciekle.html", bolumler=bolumler)
    
@app.route("/ogrenci/sil/<int:id>")
@login_required
def ogrenci_sil(id):
    op.sil(id)
    flash("Öğrenci Silme Başarılı", "success")
    return redirect(url_for("ogrenciler"))
@app.route("/ogrenci/guncelle/<int:id>", methods=["GET", "POST"])
@login_required
def ogrenci_guncelle(id):
    ogrenci = op.bul(id)

    if request.method == "POST":
        ad = request.form.get("ad")
        soyad = request.form.get("soyad")
        bolumid = request.form.get("bolumid")
        op.guncelle(id, ad, soyad, bolumid)
        flash("Öğrenci Güncelleme Başarılı", "success")
        return redirect(url_for("ogrenciler"))
    bolumler = br.liste()
    return render_template("ogrenciguncelle.html", ogrenci=ogrenci, bolumler=bolumler)

@app.route("/login" ,methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password_entered = request.form.get("password")
        if not username or not password_entered:
            flash("Tüm alanları doldurun", "danger")
            return render_template("giris.html")

        user = up.login(username)
        if not user:
            flash("Yanlış kullanıcı adı veya şifre", "danger")
            return render_template("giris.html")

        password_cryted = user["password"]
        if sha256_crypt.verify(password_entered, password_cryted):
            session["logged_in"] = True
            session["username"] = username
            flash("Login Başarılı ...", "success")
            return redirect(url_for("index"))

        flash("Yanlış kullanıcı adı veya şifre", "danger")
    return render_template("giris.html")
       
@app.route("/logout")
def logout():
    return up.logout()
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
    bolumler = br.liste()
    return render_template("bolumlist.html", bolumler=bolumler)

@app.route("/bolum/ekle" , methods=["GET", "POST"])
@login_required
def bolum_ekle():
    if request.method == "POST":
        bolumad = request.form.get("bolumad")
        br.ekle(bolumad)
        flash("Bölüm Ekleme Başarılı", "success")
        return redirect(url_for("bolumler"))
    return render_template("bolumekle.html")
@app.route("/bolum/guncelle/<int:id>", methods=["GET", "POST"])

@login_required
def bolum_guncelle(id):
     

    bolum = br.bul(id)

    if request.method == "POST":
        bolumad = request.form.get("bolumad")
        print(bolumad)
        br.guncelle(id, bolumad)
        flash("Bölüm Güncelleme Başarılı", "success")
        return redirect(url_for("bolumler"))

    return render_template("bolumguncelle.html", bolum=bolum)

@app.route("/bolum/sil/<int:id>" )
@login_required
def bolum_sil(id):
    br.sil(id)
    flash("Bölüm Silme Başarılı", "success")
    return redirect(url_for("bolumler"))

if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)