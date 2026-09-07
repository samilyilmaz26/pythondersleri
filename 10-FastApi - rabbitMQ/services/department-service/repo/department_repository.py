from repo.base_repository import BaseRepository
from models.department import Department


class DepartmentRepository(BaseRepository):
    """Data access for the department table."""

    def list_all(self) -> list[Department]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from department").fetchall()
            return [Department.from_row(row) for row in rows]

    def find(self, id) -> Department | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from department where id = ?", (id,)
            ).fetchone()
            return Department.from_row(row)

    def add(self, name) -> int:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("insert into department (name) values (?)", (name,))
            return cursor.lastrowid

    def update(self, id, name) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("update department set name = ? where id = ?", (name, id))

    def delete(self, id) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from department where id = ?", (id,))
