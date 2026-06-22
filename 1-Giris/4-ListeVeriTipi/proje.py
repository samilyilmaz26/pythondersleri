# Listeler strinden farklı olarak değiştirilebilir
listeSayi = [1,10,100,55,77]
print(listeSayi)
listeMeyva = ["Elma" ,"Armut " ,"Muz"]
print(listeMeyva)
listeKarma = ["Elma" , 123 ,"Portakal"]
print(listeKarma)
liste = [3,4,5,6,6,7,8,9,0,0,0,300]
print(len(liste))

selam = "Merhaba"
ls = list(selam)
print(ls)
liste = [1,2,3,4,5,6,7,8,9,10]
print(liste[4])
print(liste[len(liste)-1])
print(liste[1:5])
print(liste[0:7:2])
print(liste[::2])
print(liste[::-1])
 
l1 =  [1,2,3,4,5]
l2 =  [6,7,8,9,10]
print(l1+ l2)

meyvalar =["Elma" ,"Armut","Muz"]
print(meyvalar*3)
meyvalar.append("Portakal")
print(meyvalar)
meyvalar.pop()
print(meyvalar)
meyvalar.pop(1)
print(meyvalar)

meyvalar2 =["Elma" ,"Armut","Muz"]
meyvalar2.sort()
print(meyvalar2)
meyvalar2.sort(reverse=True)
print(meyvalar2)

liste1 = [1,2,3]
liste2 = [4,5,6]
liste3 = [7,8,9]
tls  = [liste1 , liste2 ,liste3]
 
print(tls[1][2])
 