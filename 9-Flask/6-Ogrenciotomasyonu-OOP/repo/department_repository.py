from repo.base_repository import BaseRepository
from models.department import Department


class DepartmentRepository(BaseRepository):
    """Data access for the Bolum (department) table."""

    def list_all(self) -> list[Department]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from Bolum").fetchall()
            return [Department.from_row(row) for row in rows]

    def add(self, bolumad):
        with self.db as con:
            cursor = con.cursor()
            cmd = "insert into Bolum (bolumad) values (?)"
            cursor.execute(cmd, (bolumad,))

    def delete(self, id):
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from Bolum where id = ?", (id,))

    def find(self, id) -> Department | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from Bolum where id = ?", (id,)
            ).fetchone()
            return Department.from_row(row)

    def update(self, id, bolumad):
        with self.db as con:
            cursor = con.cursor()
            cmd = "update Bolum set bolumad = ? where id = ?"
            cursor.execute(cmd, (bolumad, id))
