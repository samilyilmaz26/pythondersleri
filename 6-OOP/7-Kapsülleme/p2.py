class BankaHesabi:
    def __init__(self, id ,hesap_sahibi, kkno):
        self.id = id
        self.hesap_sahibi = hesap_sahibi         
        self.__kkno = kkno              

    # GETTER: Gizli olan kknoyi güvenli bir şekilde dışarıya göstermek için
    def kkno_goster(self):
        return str(self.__kkno)[0:4] + "****"  # İlk 4 rakamı göster, geri kalanını gizle
 