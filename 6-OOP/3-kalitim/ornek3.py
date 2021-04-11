class Temel():
    def __init__(self, ad, soyad ,cadde ,ilce,sehir):
        self.ad = ad
        self.soyad = soyad
        self.ilce = ilce
        self.sehir = sehir
        self.cadde = cadde
    def adresyaz(self):
        print("Sayın: {}\n {}\n {}\n{}".format(self.fullname(), self.cadde,self.ilce,self.sehir))
    def fullname(self):
        return self.ad + " " + self.soyad

class Ogrenci(Temel):
    pass

ogrenci = Ogrenci(ad ="Mehmet", soyad="Yılmaz",cadde="Bahariye cad", ilce="Kadıköy",sehir = "İstanbul")
ogrenci.adresyaz() 
ogrenci.fullname()

class Egitmen(Temel):
    def __init__(self, ad, soyad ,cadde ,ilce,sehir,maas,unvan):
        super().__init__(ad, soyad ,cadde ,ilce,sehir)
        self.maas = maas
        self.unvan = unvan
    def fullname(self):
        return self.unvan + " "+  self.ad + " " + self.soyad
    def maasyaz(self):
        print(self.maas)
    
egitmen = Egitmen(ad ="Şamil", soyad="Yılmaz",cadde="Bahariye cad", 
ilce="Kadıköy",sehir = "İstanbul",maas= 3000, unvan= "Doçent.Dr")
 

egitmen.adresyaz()
egitmen.fullname()
egitmen.maasyaz()