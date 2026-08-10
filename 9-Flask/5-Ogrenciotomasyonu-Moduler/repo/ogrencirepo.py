from repo.connection import opendb

@opendb
def liste(con):
    cursor = con.cursor()
    cmd = "select o.id, o.ad, o.soyad, b.bolumad from Ogrenci o inner join Bolum b on (o.Bolumid = b.id)"
    ogrenci_tuple = cursor.execute(cmd).fetchall()
    ogrenciler= []
    for ogrenci in ogrenci_tuple:
        ogrenciler.append(dict(ogrenci))
    #ogrenciler = [dict(row) for row in ogrenci_tuple]
    return ogrenciler
@opendb
def ekle(con, ad, soyad, bolumid):
    cursor = con.cursor()
    cmd = "insert into Ogrenci (ad,soyad,Bolumid) values (?,?,?)"
    cursor.execute(cmd, (ad, soyad, bolumid))
    con.commit()
@opendb
def sil(con, id):
    cursor = con.cursor()
    cmd = "delete from Ogrenci where id = ?"
    cursor.execute(cmd, (id,))
    con.commit() 
@opendb
def bul(con, id):
    cursor = con.cursor()
    cmd = "select * from Ogrenci where id = ?"
    result = cursor.execute(cmd, (id,)).fetchone()
    if result:
        return dict(result)
    else:
        return None
@opendb
def guncelle(con, id, ad, soyad, bolumid):
    cursor = con.cursor()
    cmd = "update Ogrenci set ad = ?, soyad = ?, Bolumid = ? where id = ?"
    cursor.execute(cmd, (ad, soyad, bolumid, id))
    con.commit()
