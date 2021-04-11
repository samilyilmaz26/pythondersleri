import sqlite3
con = sqlite3.connect("personel.db")
cursor = con.cursor() 

# def Listele2():
#     cursor.execute('select * from personel')
#     olist  = cursor.fetchall()
#     for i in olist:
#         print(i)

def Listele():
    cursor.execute('select * from personel')
 
    row = list(zip(cursor.description))
     
    olist  = cursor.fetchall()
    print(row)
     
    selen = dict(zip(row, olist))
    print(selen)    
 

# def Ekle(ad,soyad,maas):
#     cursor.execute('insert into personel (ad,soyad ,maas) values(? , ? ,?)', (ad,soyad,maas))
#     con.commit()
# ad = input("Adı :")
# soyad  = input("Soyad :")
# maas = input("Maaş :")
# Ekle(ad,soyad,maas)

# def Guncel(id ,maas):
#     cursor.execute('update  personel set maas = ?  where id =? ', (maas,id))
#     con.commit()
# id = input("id  :")
# maas = int(input("Maaş :")) 
# Guncel(id ,maas)


# def Sil(id ):
#     cursor.execute('delete from   personel  where id =? ', (id,))
#     con.commit()
# id = input("id  :")
# Sil(id)
Listele()
 


