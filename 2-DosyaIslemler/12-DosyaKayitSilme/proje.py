import os
with open("dosya.txt", "r+" ,encoding = "utf-8") as dosya:
    liste  = dosya.readlines()
    print(liste)
    liste.remove("Egitim\n")
    for i in liste:
        print (i)
    dosya.close()
    os.remove("dosya.txt")
    
with open("dosya.txt", "a" ,encoding = "utf-8") as dosya:  
    dosya.seek(0) 
    for i in liste:
        dosya.write(i)
dosya.close
   