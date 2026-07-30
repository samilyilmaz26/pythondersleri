import sqlite3
con = sqlite3.connect("kampus.db")
cursor = con.cursor()

class Temel():
    def __init__(self,id, ad, soyad , ilce, sehir):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.ilce = ilce
        self.sehir = sehir

    def tam_ad(self):
        return f"{self.ad} {self.soyad}"
    def adres(self):
        return f" {self.ilce}-{self.sehir.upper()}"
class Ogrenci(Temel):
    pass
class Ogretmen(Temel):
    def __init__(self, id, ad, soyad, ilce, sehir, unvan):
        super().__init__(id, ad, soyad, ilce, sehir)
        self.unvan = unvan

    def tam_ad(self):
        return f"{self.unvan} {self.ad} {self.soyad}"
    
class Calisan(Temel):   
    def __init__(self, id, ad, soyad, ilce, sehir, departman):
        super().__init__(id, ad, soyad , ilce, sehir)
        self.departman = departman
    def departman_bilgisi(self):
        return f"{self.departman} "
def ogreci_bilgisi(id):
    cursor.execute("SELECT * FROM ogrenci where id=?", (id,))
    ogrenci = cursor.fetchone()  
    return Ogrenci(*ogrenci)
def ogretmen_bilgisi(id):
    cursor.execute("SELECT * FROM egitmen where id=?", (id,))
    ogretmen = cursor.fetchone()  
    return Ogretmen(*ogretmen)
def calisan_bilgisi(id):
    try:
        cursor.execute("SELECT * FROM calisan where id=?", (id,))
        calisan = cursor.fetchone()  
        return Calisan(*calisan)
    except TypeError:
        print("Çalışan bulunamadı.")
  
while True:
    secim= input("""
1- öğrenci Bilgisi
2- Öğretmen Bilgisi
3- Çalışan Bilgisi
9- Çıkış

 """)
    if secim == "1":
        id = input("Öğrenci ID'sini girin: ")
        ogrenci = ogreci_bilgisi(id)
        print(ogrenci.tam_ad())
        print(ogrenci.adres())  
    elif secim == "2":
        id = input("Öğretmen ID'sini girin: ")
        ogretmen = ogretmen_bilgisi(id)
        print(ogretmen.tam_ad())
        print(ogretmen.adres())
    elif secim == "3":
        id = input("Çalışan ID'sini girin: ")
        calisan = calisan_bilgisi(id)
        print(calisan.tam_ad())
        print(calisan.adres())
        print(calisan.departman_bilgisi())  
       