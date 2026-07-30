import sqlite3


class Ogrenci():

    def __init__(self, id, ad, soyad, DogumTarih):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.DogumTarih = DogumTarih

    def __str__(self):
        return "Id: {}\nAd: {}\nSoyad {}\nDogumTarih: {}".format(self.id, self.ad, self.soyad, self.DogumTarih)


class Libs():
     

   
    def Liste(self):
        sorgu = "Select * from Ogrenciler"
        self.cursor.execute(sorgu)
        olist = self.cursor.fetchall()
        for i in olist:
            ogrenci = Ogrenci(*i)
            print(ogrenci)
    def ListbyName(self):
         isim  =   input(" İsim giriniz")
         sorgu = 'select * from ogrenci where ad = ? '
         self.cursor.execute(sorgu,(isim,))
         olist =self.cursor.fetchall()
         for i in olist:
              ogrenci = Ogrenci(*i)
              print(ogrenci)
    def Sil(self):
        id = int(input("Id Giriniz"))
        sorgu = 'delete  from ogrenci where id = ? '
        self.cursor.execute(sorgu, (id,))
        self.cursor.commit();
    def Guncel(self):
        id = input("Id Giriniz")
        isim = input('Yeni İsmi Giriniz')
        sorgu = 'update ogrenci set ad = ?  where id = ? '
        self.cursor.execute(sorgu, (isim,id))
        self.cursor.commit();
    def Ekle(self):
        ad = input("Ad  Giriniz")
        soyad = input("soyad   Giriniz")
        dtar = input("Doğum Tarihi Giriniz")
        sorgu = 'insert into ogrenci (ad,soyad ,DogumTarih) values (? ,?,? ) '
        self.cursor.execute(sorgu, (ad, soyad ,dtar))
        self.cursor.commit();

