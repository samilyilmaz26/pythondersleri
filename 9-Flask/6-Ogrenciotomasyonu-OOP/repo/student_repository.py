from repo.base_repository import BaseRepository
from models.student import Student


class StudentRepository(BaseRepository):
    """Data access for the Ogrenci (student) table."""

    def list_all(self) -> list[Student]:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "select o.id, o.ad, o.soyad, o.bolumid, b.bolumad, "
                "o.mahalle, o.cadde, o.kapino, o.city "
                "from Ogrenci o inner join Bolum b on (o.bolumid = b.id)"
            )
            rows = cursor.execute(cmd).fetchall()
            return [Student.from_row(row) for row in rows]

    def add(self, student: Student) -> None:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "insert into Ogrenci (ad, soyad, bolumid, mahalle, cadde, kapino, city) "
                "values (?, ?, ?, ?, ?, ?, ?)"
            )
            cursor.execute(
                cmd,
                (
                    student.ad,
                    student.soyad,
                    student.bolumid,
                    student.mahalle,
                    student.cadde,
                    student.kapino,
                    student.city,
                ),
            )

    def delete(self, id):
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from Ogrenci where id = ?", (id,))

    def find(self, id) -> Student | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from Ogrenci where id = ?", (id,)
            ).fetchone()
            return Student.from_row(row)

    def update(self, student: Student) -> None:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "update Ogrenci set ad = ?, soyad = ?, bolumid = ?, "
                "mahalle = ?, cadde = ?, kapino = ?, city = ? where id = ?"
            )
            cursor.execute(
                cmd,
                (
                    student.ad,
                    student.soyad,
                    student.bolumid,
                    student.mahalle,
                    student.cadde,
                    student.kapino,
                    student.city,
                    student.id,
                ),
            )
