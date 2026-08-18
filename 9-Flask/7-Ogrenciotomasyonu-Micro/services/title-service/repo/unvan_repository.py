from repo.base_repository import BaseRepository
from models.unvan import Unvan


class UnvanRepository(BaseRepository):
    """Data access for the Unvan (instructor title) table."""

    def list_all(self) -> list[Unvan]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from Unvan").fetchall()
            return [Unvan.from_row(row) for row in rows]

    def add(self, unvan: Unvan) -> int:
        with self.db as con:
            cursor = con.cursor()
            cmd = "insert into Unvan (unvanad) values (?)"
            cursor.execute(cmd, (unvan.unvanad,))
            return cursor.lastrowid

    def delete(self, id):
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from Unvan where id = ?", (id,))

    def find(self, id) -> Unvan | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from Unvan where id = ?", (id,)
            ).fetchone()
            return Unvan.from_row(row)

    def update(self, unvan: Unvan) -> None:
        with self.db as con:
            cursor = con.cursor()
            cmd = "update Unvan set unvanad = ? where id = ?"
            cursor.execute(cmd, (unvan.unvanad, unvan.id))
