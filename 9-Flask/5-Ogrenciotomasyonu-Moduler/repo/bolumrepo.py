from repo.connection import opendb

@opendb
def liste(con):
    cursor = con.cursor()
    sorgu = "select * from bolum"
    bolum_tuple = cursor.execute(sorgu).fetchall()
    bolumler = [dict(row) for row in bolum_tuple]
    return bolumler
@opendb
def bolum_ekle(con, bolumad):
    cursor = con.cursor()
    cmd = "insert into bolum (bolumad) values (?)"
    cursor.execute(cmd, (bolumad,))
    con.commit()

@opendb
def sil(con, id):
    cursor = con.cursor()
    cmd = "delete from bolum where id = ?"
    cursor.execute(cmd, (id,))
    con.commit()
@opendb
def  bul(con, id):
    cursor = con.cursor()
    cmd = "select * from bolum where id = ?"
    result = cursor.execute(cmd, (id,)).fetchone()
    if result:
        return dict(result)
    else:
        return None

@opendb
def bolum_guncelle(con, id, bolumad):
    cursor = con.cursor()
    cmd = "update bolum set bolumad = ? where id = ?"
    cursor.execute(cmd, (bolumad, id))
    con.commit()
