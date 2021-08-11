dosya = open("dosya.txt", "r", encoding="utf-8")

bilgiler = dosya.readlines()
print(type(bilgiler))

print(bilgiler)

for i in bilgiler:
    print(i, end = "")
 

dosya.close() 