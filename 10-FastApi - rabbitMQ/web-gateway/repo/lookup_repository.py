from repo.base_repository import BaseRepository


class LookupRepository(BaseRepository):
    """Local id -> name cache for cities and departments.

    Kept in sync via RabbitMQ events so the events consumer can resolve
    cityname/departmentname for incoming student events without calling
    city-service/department-service over HTTP.
    """

    def create_tables(self) -> None:
        with self.db as con:
            con.execute("CREATE TABLE IF NOT EXISTS city_lookup (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
            con.execute(
                "CREATE TABLE IF NOT EXISTS department_lookup (id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
            )

    def upsert_city(self, id, name) -> None:
        with self.db as con:
            con.execute(
                "INSERT INTO city_lookup (id, name) VALUES (?, ?) "
                "ON CONFLICT(id) DO UPDATE SET name = excluded.name",
                (id, name),
            )

    def delete_city(self, id) -> None:
        with self.db as con:
            con.execute("DELETE FROM city_lookup WHERE id = ?", (id,))

    def get_city_name(self, id):
        if id is None:
            return None
        with self.db as con:
            row = con.execute("SELECT name FROM city_lookup WHERE id = ?", (id,)).fetchone()
            return row["name"] if row else None

    def upsert_department(self, id, name) -> None:
        with self.db as con:
            con.execute(
                "INSERT INTO department_lookup (id, name) VALUES (?, ?) "
                "ON CONFLICT(id) DO UPDATE SET name = excluded.name",
                (id, name),
            )

    def delete_department(self, id) -> None:
        with self.db as con:
            con.execute("DELETE FROM department_lookup WHERE id = ?", (id,))

    def get_department_name(self, id):
        if id is None:
            return None
        with self.db as con:
            row = con.execute("SELECT name FROM department_lookup WHERE id = ?", (id,)).fetchone()
            return row["name"] if row else None
