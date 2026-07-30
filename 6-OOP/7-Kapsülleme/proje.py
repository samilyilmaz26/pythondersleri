class BankaHesabi:
    def __init__(self, hesap_sahibi, kkno):
        self.hesap_sahibi = hesap_sahibi        # Kamu (Public) değişken
        self.__kkno = kkno                  # Gizli (Private) değişken (Dışarıdan erişilemez)

    # GETTER: Gizli olan kknoyi güvenli bir şekilde dışarıya göstermek için
    def kkno_goster(self):
        return str(self.__kkno)[0:4] + "****"  # İlk 4 rakamı göster, geri kalanını gizle

# ---- Sınıfı Kullanalım ----

hesap = BankaHesabi("Ahmet Yılmaz", 58302520 )

# 1. Kamu (Public) değişkene doğrudan erişebiliriz
print("Hesap Sahibi:", hesap.hesap_sahibi)  # Çıktı: Ahmet Yılmaz

# 2. Gizli (Private) değişkene doğrudan erişmeye çalışalım (Hata verecektir)
#print(hesap.__kkno)  # <-- Bu satır AttributeError hatası verir!

# 3. Getter metodu ile kknoyi güvenli bir şekilde görelim
print("Mevcut kkno:", hesap.kkno_goster())  # v

 