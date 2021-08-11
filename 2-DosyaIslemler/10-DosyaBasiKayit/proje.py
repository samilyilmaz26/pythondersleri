with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:
    icerik = dosya.read()
    icerik = "Başa Yeni Kayıt Eklendi\n" +icerik
    dosya.seek(0)
    dosya.write(icerik)
    dosya.close()
with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:
    icerik = dosya.read() 
    print(icerik)  
