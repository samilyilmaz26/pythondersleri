from  flask import Flask,render_template,redirect,url_for,request,flash,session
import sqlite3
from forms import RegistrationForm,LoginForm,ArticleForm
from passlib.hash import sha256_crypt
from decorators import login_required,admin_required
from ConverToDict import  dict_factory
from datetime import date 

app= Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin')
@admin_required
def admin():
    return render_template("admin.html")

@app.route('/index')
def main():
    return redirect(url_for("index"))

@app.route('/about')
def about():
    sirket ="Abc Limited Şirketi"
    return render_template("about.html", sirket= sirket)

@app.route('/article/articles')
def article():
    con = sqlite3.connect("blog.db")
    con.row_factory = dict_factory
    cursor = con.cursor()
    sorgu = "select * from articles order by id desc"
    articles = cursor.execute(sorgu).fetchall()
    print(articles)
    return render_template("/article/articles.html" ,articles = articles)
    
@app.route('/article/dashboard')
@login_required
def dashboard():
    con = sqlite3.connect("blog.db")
    con.row_factory = dict_factory
    cursor = con.cursor()
    sorguadm = "select * from articles"
    sorgu = "select * from articles where author = ?"
    role = str(session["role"])
    if role == "admin":
        result = cursor.execute(sorguadm)
        return render_template("/article/dashboard.html" ,articles = result)
    else:
        result = cursor.execute(sorgu, (session["username"],)).fetchall()
        return render_template("/article/dashboard.html" ,articles = result)
@app.route('/article/detail/<string:id>') 
def detail( id):
    con = sqlite3.connect("blog.db")  
    con.row_factory = dict_factory
    cursor = con.cursor()
    sorgu = 'select * from articles where id = ?'
    article = cursor.execute(sorgu,(id,)).fetchone()
    print(article)
    return render_template("/article/detail.html", article = article)
@app.route('/article/addarticle',methods=["GET","POST"])
@login_required
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST":
        title = form.title.data
        content = form.content.data
        con =  sqlite3.connect("blog.db")
        cursor = con.cursor()
        sorgu = "insert into articles (author,title, content, created_date) values(?,?,?,?) "
        cursor.execute(sorgu,(session["username"],title,content,date.today()) )
        con.commit()
        con.close()
        flash("Makale Eklendi ...","success")
        return redirect(url_for("dashboard"))
    else:
        return render_template("/article/addarticle.html", form = form)

@app.route("/article/edit/<string:id>",methods=["GET","POST"])
@login_required
def edit(id):
    if request.method == "GET":
        form = ArticleForm(request.form)
        baslik = "Makale Güncelleme"
        btntext = "Güncelle"
        con  = sqlite3.connect("blog.db")
        con.row_factory = dict_factory
        cursor = con.cursor()
        sorgu = 'select * from articles where id = ?'
        article = cursor.execute(sorgu,(id,)).fetchone()
        form.content.data = article["content"]
        form.title.data = article["title"]
        con.close()
        return render_template("/article/edit.html" , form = form,baslik = baslik , btntext = btntext)
    else:
        form = ArticleForm(request.form)
        content = form.content.data
        title = form.title.data
        con = sqlite3.connect("blog.db")
        cursor = con.cursor()
        sorgu = "update articles set title = ? , content = ? where id = ?"
        cursor.execute(sorgu, (title,content,id))
        con.commit()
        flash("Güncelleme Başarılı", "success")
        con.close()
        return  redirect(url_for("dashboard"))
@app.route("/article/delete/<string:id>",methods=["GET","POST"])
@login_required
def delete(id):
    if request.method == "GET":
        form = ArticleForm(request.form)
        baslik = "Makale Silinecek Eminmisiniz"
        btntext = "Sil"
        con  = sqlite3.connect("blog.db")
        con.row_factory = dict_factory
        cursor = con.cursor()
        sorgu = 'select * from articles where id = ?'
        article = cursor.execute(sorgu,(id,)).fetchone()
        print(article)
        form.content.data = article["content"]
        form.title.data = article["title"]
        con.close()
        return render_template("/article/edit.html" , form = form, baslik = baslik, btntext = btntext)
    else:
        form = ArticleForm(request.form)
        con = sqlite3.connect("blog.db")
        cursor = con.cursor()
        sorgu = " delete from articles where id = ?"
        cursor.execute(sorgu, (id,))
        con.commit()
        flash("Silme İşlemi Başarılı ", "success")
        con.close()
        return  redirect(url_for("dashboard"))        

@app.route('/login' ,methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method =="POST":
        username = form.username.data
        password_entered = form.password.data
        con = sqlite3.connect("blog.db")
        cursor = con.cursor()
        sorgu = 'select * from user where username = ?'
        result = cursor.execute(sorgu,(username,)).fetchone()
        if result:
            password_real = result[3]
            session["role"] = " "
            if sha256_crypt.verify(password_entered, password_real):
                session["logged_in"] = True
                session["username"] = username
                session["role"] = result[4]
                print(session["role"])
                flash("Giriş İşlemi Başarılı","success")
                con.close()
                return redirect(url_for("dashboard"))
            else:
                flash("Yanlış Şifre ","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı yok","danger")
            return redirect(url_for("login"))
    else:
        return render_template("/login.html",form = form)
@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Çıkış İşlemi Başarılı","success")
    return redirect(url_for("index"))
@app.route('/register' ,methods=["GET","POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method =="POST" and form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        con = sqlite3.connect('blog.db')
        cursor = con.cursor()
        sorgu = "select * from user where email = ?"
        usermailcheck = cursor.execute(sorgu, (email,)).fetchone()
        if usermailcheck:
            flash("Bu mail adresi sistemde kayıtlı", "danger")
            return render_template("/register.html", form=form)
        else:
            sorgu = "select * from user where username = ?"
            usernamecheck =  cursor.execute(sorgu, (username,)).fetchone()
            if usernamecheck:
                flash("Bu kullanıcı  sistemde kayıtlı", "danger")
                return render_template("/register.html", form=form)
            else:
                cursor.execute('insert into user (username,email,password) values(?,?,?)',(username,email,password))
                con.commit()
                cursor.close()
                flash("Kayıt İşlemi Başarılı ", "success")
                return redirect(url_for("index"))
    else:
        return render_template("/register.html", form=form)
if __name__ == "__main__":
    app.secret_key  ="secret"
    app.run(debug=True)