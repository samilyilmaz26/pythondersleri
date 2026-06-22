def movezeroes(*sayilar):
    liste = []
    for i in sayilar:
        if i != 0:
            liste.append(i)
    for i in range(len(sayilar)-len(liste)):
        liste.append(0)
    return liste

x = movezeroes(1,5,0,20,0,7)
print(x)
    

    
