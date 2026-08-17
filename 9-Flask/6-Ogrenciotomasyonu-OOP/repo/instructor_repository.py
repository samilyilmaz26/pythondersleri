from repo.base_repository import BaseRepository
from models.instructor import Instructor


class InstructorRepository(BaseRepository):
    """Data access for the Egitmen (instructor) table."""

    def list_all(self) -> list[Instructor]:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "select e.id, e.ad, e.soyad, e.bolumid, b.bolumad, "
                "e.unvanid, u.unvanad, e.mahalle, e.cadde, e.kapino, e.city "
                "from Egitmen e "
                "inner join Bolum b on (e.bolumid = b.id) "
                "inner join Unvan u on (e.unvanid = u.id)"
            )
            rows = cursor.execute(cmd).fetchall()
            return [Instructor.from_row(row) for row in rows]

    def add(self, instructor: Instructor) -> None:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "insert into Egitmen (ad, soyad, bolumid, unvanid, mahalle, cadde, kapino, city) "
                "values (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            cursor.execute(
                cmd,
                (
                    instructor.ad,
                    instructor.soyad,
                    instructor.bolumid,
                    instructor.unvanid,
                    instructor.mahalle,
                    instructor.cadde,
                    instructor.kapino,
                    instructor.city,
                ),
            )

    def delete(self, id):
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from Egitmen where id = ?", (id,))

    def find(self, id) -> Instructor | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from Egitmen where id = ?", (id,)
            ).fetchone()
            return Instructor.from_row(row)

    def update(self, instructor: Instructor) -> None:
        with self.db as con:
            cursor = con.cursor()
            cmd = (
                "update Egitmen set ad = ?, soyad = ?, bolumid = ?, unvanid = ?, "
                "mahalle = ?, cadde = ?, kapino = ?, city = ? where id = ?"
            )
            cursor.execute(
                cmd,
                (
                    instructor.ad,
                    instructor.soyad,
                    instructor.bolumid,
                    instructor.unvanid,
                    instructor.mahalle,
                    instructor.cadde,
                    instructor.kapino,
                    instructor.city,
                    instructor.id,
                ),
            )
