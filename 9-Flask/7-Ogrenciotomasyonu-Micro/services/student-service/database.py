import sqlite3


class Database:
    """Encapsulates SQLite connection handling.

    Used as a context manager so every repository opens exactly one
    connection per operation and it is always closed afterwards:

        with Database() as con:
            con.execute(...)

    On a clean exit the transaction is committed; if an exception is
    raised inside the `with` block it is rolled back instead, and the
    exception is left to propagate.
    """

    def __init__(self, db_path="data.db"):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is None:
            return False
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()
        return False  # never suppress exceptions
