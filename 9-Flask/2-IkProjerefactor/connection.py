import sqlite3
from functools import wraps

import sqlite3
from functools import wraps

def opendb(func):
    """Decorator to automatically open and safely close the database connection."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Open connection and configure row factory
        con = sqlite3.connect("IK.db")
        con.row_factory = sqlite3.Row
        try:
            return func(con, *args, **kwargs)
        finally:
            con.close()
    return wrapper

 