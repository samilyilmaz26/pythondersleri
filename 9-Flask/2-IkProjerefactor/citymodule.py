from connection import opendb
@opendb
def list(con):
    cursor = con.cursor()
    sorgu = "select * from city"
    cities_tuple = cursor.execute(sorgu).fetchall()
    cities = [dict(row) for row in cities_tuple]
    return cities
@opendb
def add( con,name):
    cursor = con.cursor()
    sorgu = 'insert into city (name) values (?)'
    cursor.execute(sorgu, (name, ))
    con.commit()
@opendb    
def delete(id):
    con = opendb()
    cursor = con.cursor()


