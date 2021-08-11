dosya = open("dosya.txt", "r", encoding="utf-8")

bilgiler = dosya.readline()

print(bilgiler)
    
dosya.close() 