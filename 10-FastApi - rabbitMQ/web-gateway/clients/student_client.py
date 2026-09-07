from clients.base_client import BaseClient


class StudentClient(BaseClient):
    """HTTP client for student-service's JSON API."""

    async def list_all(self) -> list[dict]:
        return await self._get("/students")

    async def find(self, id: int) -> dict | None:
        return await self._get(f"/students/{id}") 

    async def add(
        self,
        name: str,
        surname: str | None = None,
        street: str | None = None,
        number: str | None = None,
        cityid: int | None = None,
        departmentid: int | None = None,
    ) -> dict:
        return await self._post(
            "/students",
            {
                "name": name,
                "surname": surname,
                "street": street,
                "number": number,
                "cityid": cityid,
                "departmentid": departmentid,
            },
        )

    async def update(
        self,
        id: int,
        name: str,
        surname: str | None = None,
        street: str | None = None,
        number: str | None = None,
        cityid: int | None = None,
        departmentid: int | None = None,
    ) -> dict:
        return await self._put(
            f"/students/{id}",
            {
                "name": name,
                "surname": surname,
                "street": street,
                "number": number,
                "cityid": cityid,
                "departmentid": departmentid,
            },
        )

    async def delete(self, id: int) -> None:
        await self._delete(f"/students/{id}")
