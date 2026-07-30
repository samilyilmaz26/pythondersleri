class Temel():
    def __init__(self, ad, soyad , cadde, ilce, sehir):
        self.ad = ad
        self.soyad = soyad
        self.cadde = cadde
        self.ilce = ilce
        self.sehir = sehir

    def tam_ad(self):
        return f"{self.ad} {self.soyad}"
    def adres(self):
        return f"{self.cadde} {self.ilce}-{self.sehir.upper()}"
    
class Ogrenci(Temel):
    pass
  
o1 = Ogrenci("Ali", "Yılmaz", "Atatürk Cad.", "Merkez", "Ankara")
print(o1.tam_ad())
print(o1.adres())

class Ogretmen(Temel):
    def __init__(self, ad, soyad, cadde, ilce, sehir, unvan):
        super().__init__(ad, soyad, cadde, ilce, sehir)
        self.unvan = unvan

    def tam_ad(self):
        return f"{self.unvan} {self.ad} {self.soyad}"   
class Calisan(Temel):
    def __init__(self, ad, soyad, cadde, ilce, sehir, maas, departman):
        super().__init__(ad, soyad, cadde, ilce, sehir)
        self.maas = maas
        self.departman = departman
    def departman_bilgisi(self):
        return f"{self.departman} "
    def maas_bilgisi(self):
        return f"{self.maas} TL"
 
ogretmen1 = Ogretmen("Mehmet", "Kaya", "Cumhuriyet Cad.", "Merkez", "İstanbul", "Dr.")
print(ogretmen1.tam_ad())
print(ogretmen1.adres())
calisan1 = Calisan("Ahmet", "Yılmaz", "Atatürk Cad.", "Merkez", "Ankara", 5000, "İnsan Kaynakları")
print(calisan1.tam_ad())
print(calisan1.adres())
print(calisan1.departman_bilgisi())
print(calisan1.maas_bilgisi())