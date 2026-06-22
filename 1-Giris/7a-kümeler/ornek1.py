Liste = ["Elma","Armut","Portakal","Elma"]
x= set(Liste)
print(x)
kume = {"Ali","Veli","Ali"}
print(kume)
kume = {"Ali","Veli","Ahmet" }
for i in kume:
    print(i)
ls = list(kume) #herhangi bir index ulaşmak için once list tipine çevrilir
print(ls[1])

yasakli_kelimeler = frozenset(["küfür", "argo", "spam"])
 