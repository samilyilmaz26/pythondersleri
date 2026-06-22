from  personelModule import Egitmen,Ogrenci

    
egitmen = Egitmen(ad ="Şamil", soyad="Yılmaz",cadde="Bahariye cad", 
ilce="Kadıköy",sehir = "İstanbul",maas= 3000, unvan= "Doçent.Dr")

ogrenci = Ogrenci(ad ="Mehmet", soyad="Yılmaz",cadde="Bahariye cad", ilce="Kadıköy",sehir = "İstanbul")

#egitmenadres = egitmen.adresal()
ogrenciadres = ogrenci.adresal()

for i in ogrenciadres:
    print(i)

for i in egitmen.adresal():
    print(i)