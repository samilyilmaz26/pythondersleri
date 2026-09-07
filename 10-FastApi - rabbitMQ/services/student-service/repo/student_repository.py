from repo.base_repository import BaseRepository
from models.student import Student


class StudentRepository(BaseRepository):
    """Data access for the students table."""

    def list_all(self) -> list[Student]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from students").fetchall()
            return [Student.from_row(row) for row in rows]

    def find(self, id) -> Student | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from students where id = ?", (id,)
            ).fetchone()
            return Student.from_row(row)

    def add(self, name, surname=None, street=None, number=None, cityid=None, departmentid=None) -> int:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute(
                "insert into students (name, surname, street, number, cityid, departmentid) "
                "values (?, ?, ?, ?, ?, ?)",
                (name, surname, street, number, cityid, departmentid),
            )
            return cursor.lastrowid

    def update(self, id, name, surname=None, street=None, number=None, cityid=None, departmentid=None) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute(
                "update students set name = ?, surname = ?, street = ?, number = ?, "
                "cityid = ?, departmentid = ? where id = ?",
                (name, surname, street, number, cityid, departmentid, id),
            )

    def delete(self, id) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from students where id = ?", (id,))
