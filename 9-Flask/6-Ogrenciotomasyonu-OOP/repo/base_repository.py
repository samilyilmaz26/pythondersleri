from database import Database


class BaseRepository:
    """Base class for all repositories.

    Holds the database path and exposes `self.db` as the connection
    context manager, so subclasses just write:

        with self.db as con:
            cursor = con.cursor()
            ...
    """

    def __init__(self, db_path="Ogrenci.db"):
        self.db_path = db_path

    @property
    def db(self):
        return Database(self.db_path)
