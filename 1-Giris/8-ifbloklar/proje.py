
print(  """ *********************************
              Yaş Kontrolü
***************Yaş Kontrolü**********""")
yas = int(input("Kaç Yaşınızdasınız")) 
if yas<18:
    print("Buraya 18 yaşından küçükler giremez")
else:
    print("Hoşgeldiniz")
print(  """ **********************************
              AY Kontrolü
***************Yaş Kontrolü**********""")
ay = int(input("Kaçıncı Aydayız"))
if ay ==1:
    print ("Ocak Ayındayız")
elif ay == 2:
    print ("Şubat  Ayındayız")
elif ay == 3:
    print ("Mart   Ayındayız")
elif ay == 4:
    print ("Nisan Ayındayız")
elif ay == 5:
    print ("Mayıs Ayındayız")
elif ay == 6:
    print ("Haziran Ayındayız")
elif ay == 7:
    print ("Temmuz Ayındayız")
elif ay == 8:
    print ("Ağustos Ayındayız")
elif ay == 9:
    print ("Eylül Ayındayız")
elif ay == 10:
    print ("Ekim  Ayındayız")
elif ay == 11:
    print ("Kasım Ayındayız")
elif ay == 12:
    print ("Aralık Ayındayız")
else:
    print ("Yanlış Giriş")
    