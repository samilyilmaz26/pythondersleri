with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:
    liste  = dosya.readlines()
    print(liste)
    liste.remove("Egitim\n")
    dosya.close()
with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:  
    dosya.seek(0) 
    for i in liste:
        dosya.write(i)
   