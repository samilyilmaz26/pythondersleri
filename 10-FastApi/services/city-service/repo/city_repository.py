from repo.base_repository import BaseRepository
from models.city import City


class CityRepository(BaseRepository):
    """Data access for the cities table."""

    def list_all(self) -> list[City]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from cities").fetchall()
            return [City.from_row(row) for row in rows]

    def find(self, id) -> City | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from cities where id = ?", (id,)
            ).fetchone()
            return City.from_row(row)

    def add(self, name) -> int:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("insert into cities (name) values (?)", (name,))
            return cursor.lastrowid

    def update(self, id, name) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("update cities set name = ? where id = ?", (name, id))

    def delete(self, id) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from cities where id = ?", (id,))
