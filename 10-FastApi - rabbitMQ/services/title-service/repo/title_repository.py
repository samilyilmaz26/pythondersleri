from repo.base_repository import BaseRepository
from models.title import Title


class TitleRepository(BaseRepository):
    """Data access for the titles table."""

    def list_all(self) -> list[Title]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select * from titles").fetchall()
            return [Title.from_row(row) for row in rows]

    def find(self, id) -> Title | None:
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from titles where id = ?", (id,)
            ).fetchone()
            return Title.from_row(row)

    def add(self, name) -> int:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("insert into titles (name) values (?)", (name,))
            return cursor.lastrowid

    def update(self, id, name) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("update titles set name = ? where id = ?", (name, id))

    def delete(self, id) -> None:
        with self.db as con:
            cursor = con.cursor()
            cursor.execute("delete from titles where id = ?", (id,))
