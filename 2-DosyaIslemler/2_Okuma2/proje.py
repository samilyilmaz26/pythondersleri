dosya = open("dosya.txt", "r", encoding="utf-8")

for i in dosya:
    print(i, end= "")
    
dosya.close() 