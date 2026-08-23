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
    """
    cities = await city_client.list_all()
    for city in cities:
        lookup_repo.upsert_city(city["id"], city["name"])

    departments = await department_client.list_all()
    for department in departments:
        lookup_repo.upsert_department(department["id"], department["name"])

    students = await student_client.list_all()
    for student in students:
        cityid = student.get("cityid")
        departmentid = student.get("departmentid")
        read_model_repo.upsert(
            id=student["id"],
            name=student.get("name", ""),
            surname=student.get("surname"),
            street=student.get("street"),
            number=student.get("number"),
            cityid=cityid,
            departmentid=departmentid,
            cityname=lookup_repo.get_city_name(cityid),
            departmentname=lookup_repo.get_department_name(departmentid),
        )

    current_ids = {student["id"] for student in students}
    for existing_id in read_model_repo.list_ids():
        if existing_id not in current_ids:
            read_model_repo.delete(existing_id)
