from repo.base_repository import BaseRepository
from models.student_read_model import StudentReadModel


class StudentReadModelRepository(BaseRepository):
    """Data access for the denormalized student_read_model table.

    This table is not written to by user requests directly - it is kept
    in sync by the RabbitMQ consumer that reacts to student/city/department
    events, so /students can read a single pre-joined table instead of
    calling three services and joining in Python on every request.
    """

    def create_table(self) -> None:
        with self.db as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS student_read_model (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT,
                    street TEXT,
                    number TEXT,
                    cityid INTEGER,
                    departmentid INTEGER,
                    cityname TEXT,
                    departmentname TEXT
                )
                """
            )

    def upsert(
        self,
        id,
        name,
        surname=None,
        street=None,
        number=None,
        cityid=None,
        departmentid=None,
        cityname=None,
        departmentname=None,
    ) -> None:
        with self.db as con:
            con.execute(
                """
                INSERT INTO student_read_model
                    (id, name, surname, street, number, cityid, departmentid, cityname, departmentname)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    surname = excluded.surname,
                    street = excluded.street,
                    number = excluded.number,
                    cityid = excluded.cityid,
                    departmentid = excluded.departmentid,
                    cityname = excluded.cityname,
                    departmentname = excluded.departmentname
                """,
                (id, name, surname, street, number, cityid, departmentid, cityname, departmentname),
            )

    def bulk_upsert(self, rows) -> None:
        """Same as upsert() but for many rows in a single connection/transaction.

        `rows` is an iterable of (id, name, surname, street, number, cityid,
        departmentid, cityname, departmentname) tuples. Used by the startup
        backfill, which would otherwise open one SQLite connection per
        student - fine for a handful of rows, but opening ~100k connections
        one at a time is what made backfill hang at scale.
        """
        with self.db as con:
            con.executemany(
                """
                INSERT INTO student_read_model
                    (id, name, surname, street, number, cityid, departmentid, cityname, departmentname)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    surname = excluded.surname,
                    street = excluded.street,
                    number = excluded.number,
                    cityid = excluded.cityid,
                    departmentid = excluded.departmentid,
                    cityname = excluded.cityname,
                    departmentname = excluded.departmentname
                """,
                rows,
            )

    def delete(self, id) -> None:
        with self.db as con:
            con.execute("delete from student_read_model where id = ?", (id,))

    def bulk_delete(self, ids) -> None:
        ids = list(ids)
        if not ids:
            return
        with self.db as con:
            placeholders = ",".join("?" for _ in ids)
            con.execute(f"delete from student_read_model where id in ({placeholders})", ids)

    def update_city_name(self, cityid, cityname) -> None:
        with self.db as con:
            con.execute(
                "update student_read_model set cityname = ? where cityid = ?", (cityname, cityid)
            )

    def update_department_name(self, departmentid, departmentname) -> None:
        with self.db as con:
            con.execute(
                "update student_read_model set departmentname = ? where departmentid = ?",
                (departmentname, departmentid),
            )

    def clear_city(self, cityid) -> None:
        self.update_city_name(cityid, None)

    def clear_department(self, departmentid) -> None:
        self.update_department_name(departmentid, None)

    def list_paginated(self, limit, offset) -> list[StudentReadModel]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute(
                "select * from student_read_model order by id limit ? offset ?", (limit, offset)
            ).fetchall()
            return [StudentReadModel.from_row(row) for row in rows]

    def count(self) -> int:
        with self.db as con:
            cursor = con.cursor()
            return cursor.execute("select count(*) from student_read_model").fetchone()[0]

    def list_ids(self) -> list[int]:
        with self.db as con:
            cursor = con.cursor()
            rows = cursor.execute("select id from student_read_model").fetchall()
            return [row["id"] for row in rows]
