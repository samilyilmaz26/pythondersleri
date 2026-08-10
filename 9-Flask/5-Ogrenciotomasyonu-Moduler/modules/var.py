from flask import render_template


def get_degiskenler_data():
    isim = "Ali"
    yas = 25
    user = {"isim": "Ali", "yas": 25}
    userlist = [
        {"isim": "Ali", "yas": 25},
        {"isim": "Veli", "yas": 30},
        {"isim": "Ayşe", "yas": 20},
    ]
    return {"isim": isim, "yas": yas, "user": user, "userlist": userlist}


def degiskenler():
    data = get_degiskenler_data()
    return render_template("degiskenler.html", **data)