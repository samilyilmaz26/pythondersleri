with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:
    dosya.seek(10)
    dosya.write("Yeni Kayıt")
    print(dosya.tell())
    dosya.seek(0)
    bilgi = dosya.readlines()
    for i in bilgi:
        print(i)

  