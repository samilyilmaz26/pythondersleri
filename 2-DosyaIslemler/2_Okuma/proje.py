file = open("dosya.txt", "r", encoding="utf-8")

for i in file:
    print(i)
    
file.close() 