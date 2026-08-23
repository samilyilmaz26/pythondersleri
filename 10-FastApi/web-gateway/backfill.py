from repo.lookup_repository import LookupRepository
from repo.student_read_model_repository import StudentReadModelRepository


async def run_backfill(
    city_client,
    department_client,
    student_client,
    lookup_repo: LookupRepository,
    read_model_repo: StudentReadModelRepository,
) -> None:
    """One-time full sync from the source services into the read-model.

    Runs once at gateway startup, before the events consumer starts, so
    records created before the event system existed (or events missed
    while the gateway was down) still end up correctly denormalized.
    Idempotent: safe to run on every restart.

    Cities/departments are small lists (handful of rows), so upserting them
    one at a time is fine. Students can be large, so they are written with
    bulk_upsert/bulk_delete (single connection/transaction) instead of one
    repository call per row - looping student-by-student with per-row calls
    opens one SQLite connection per student, which is what made backfill
    hang once the table reached ~100k rows.
    """
    cities = await city_client.list_all()
    city_names = {}
    for city in cities:
        lookup_repo.upsert_city(city["id"], city["name"])
        city_names[city["id"]] = city["name"]

    departments = await department_client.list_all()
    department_names = {}
    for department in departments:
        lookup_repo.upsert_department(department["id"], department["name"])
        department_names[department["id"]] = department["name"]

    students = await student_client.list_all()

    def rows():
        for student in students:
            cityid = student.get("cityid")
            departmentid = student.get("departmentid")
            yield (
                student["id"],
                student.get("name", ""),
                student.get("surname"),
                student.get("street"),
                student.get("number"),
                cityid,
                departmentid,
                city_names.get(cityid),
                department_names.get(departmentid),
            )

    read_model_repo.bulk_upsert(rows())

    current_ids = {student["id"] for student in students}
    stale_ids = [existing_id for existing_id in read_model_repo.list_ids() if existing_id not in current_ids]
    read_model_repo.bulk_delete(stale_ids)
