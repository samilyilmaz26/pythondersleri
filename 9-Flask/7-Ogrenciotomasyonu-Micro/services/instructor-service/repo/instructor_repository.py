from repo.base_repository import BaseRepository
from models.instructor import Instructor


class InstructorRepository(BaseRepository):
    """Data access for the Egitmen (instructor) table.

    Pure CRUD on this service's own table only — department and title
    names are department-service's / title-service's responsibility,
    composed in by the gateway.
    """

    def list_all(self) -> list[Instructor]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from Egitmen").fetchall()
            return [Instructor.from_row(row) for row in rows]

    def add(self, instructor: Instructor) -> int:
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
            return cursor.lastrowid

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
