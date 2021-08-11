dosya = open("dosya.txt", "r", encoding="utf-8")

bilgiler = dosya.read()

print(bilgiler,sep="")
    
dosya.close() 