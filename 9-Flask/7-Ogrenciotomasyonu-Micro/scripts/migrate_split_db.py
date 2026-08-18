"""One-off migration: split the old monolith's Ogrenci.db into one
SQLite file per microservice, preserving the existing demo data.

Run once, before the first `docker compose up`:

    python scripts/migrate_split_db.py

Reads the root Ogrenci.db and writes, under data/:
    departments.db  (Bolum)
    titles.db       (Unvan)
    students.db     (Ogrenci)
    instructors.db  (Egitmen)
    users.db        (User)
"""
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DB = os.path.join(ROOT, "Ogrenci.db")
DATA_DIR = os.path.join(ROOT, "data")

SCHEMAS = {
    "departments.db": (
        "Bolum",
        'CREATE TABLE "Bolum" ("id" INTEGER NOT NULL UNIQUE, "bolumad" TEXT, '
        'PRIMARY KEY("id" AUTOINCREMENT))',
    ),
    "titles.db": (
        "Unvan",
        'CREATE TABLE "Unvan" ("id" INTEGER NOT NULL UNIQUE, "unvanad" TEXT, '
        'PRIMARY KEY("id" AUTOINCREMENT))',
    ),
    "students.db": (
        "Ogrenci",
        'CREATE TABLE "Ogrenci" ("id" INTEGER NOT NULL UNIQUE, "ad" TEXT, "soyad" TEXT, '
        '"bolumid" INTEGER, "mahalle" TEXT, "cadde" TEXT, "kapino" TEXT, "city" TEXT, '
        'PRIMARY KEY("id" AUTOINCREMENT))',
    ),
    "instructors.db": (
        "Egitmen",
        'CREATE TABLE "Egitmen" ("id" INTEGER NOT NULL UNIQUE, "ad" TEXT, "soyad" TEXT, '
        '"bolumid" INTEGER, "mahalle" TEXT, "cadde" TEXT, "kapino" TEXT, "city" TEXT, '
        '"unvanid" INTEGER, PRIMARY KEY("id" AUTOINCREMENT))',
    ),
    "users.db": (
        "User",
        'CREATE TABLE "User" ("id" INTEGER NOT NULL UNIQUE, "username" TEXT, '
        '"email" TEXT UNIQUE, "password" TEXT, PRIMARY KEY("id" AUTOINCREMENT))',
    ),
}


def migrate():
    if not os.path.exists(SOURCE_DB):
        raise SystemExit(f"Kaynak veritabanı bulunamadı: {SOURCE_DB}")
    os.makedirs(DATA_DIR, exist_ok=True)

    source = sqlite3.connect(SOURCE_DB)
    source.row_factory = sqlite3.Row

    for filename, (table, create_sql) in SCHEMAS.items():
        dest_path = os.path.join(DATA_DIR, filename)
        dest = sqlite3.connect(dest_path)
        dest.execute(create_sql)

        rows = source.execute(f"SELECT * FROM {table}").fetchall()
        if rows:
            columns = rows[0].keys()
            column_list = ", ".join(columns)
            placeholders = ", ".join("?" for _ in columns)
            dest.executemany(
                f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})",
                [tuple(row) for row in rows],
            )
        dest.commit()
        dest.close()
        print(f"{filename}: {len(rows)} satır aktarıldı ({table})")

    source.close()


if __name__ == "__main__":
    migrate()
