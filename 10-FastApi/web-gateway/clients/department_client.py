from clients.base_client import BaseClient


class DepartmentClient(BaseClient):
    """HTTP client for department-service's JSON API."""

    async def list_all(self) -> list[dict]:
        return await self._get("/departments")

    async def find(self, id: int) -> dict | None:
        return await self._get(f"/departments/{id}")

    async def add(self, name: str) -> dict:
        return await self._post("/departments", {"name": name})

    async def update(self, id: int, name: str) -> dict:
        return await self._put(f"/departments/{id}", {"name": name})

    async def delete(self, id: int) -> None:
        await self._delete(f"/departments/{id}")
