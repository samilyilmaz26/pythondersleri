from repo.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository):
    """Data access for the users table."""

    def find(self, id):
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from users where id = ?", (id,)
            ).fetchone()
            return User.from_row(row)

    def find_by_username(self, username):
        with self.db as con:
            cursor = con.cursor()
            row = cursor.execute(
                "select * from users where username = ?", (username,)
            ).fetchone()
            return User.from_row(row)

    def register(self, username, email, password_hash) -> int:
        with self.db as con:
            cursor = con.cursor()
            cmd = "insert into users (username, password, email) values (?, ?, ?)"
            cursor.execute(cmd, (username, password_hash, email))
            return cursor.lastrowid
