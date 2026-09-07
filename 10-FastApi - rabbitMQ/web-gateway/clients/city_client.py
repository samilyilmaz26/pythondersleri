from clients.base_client import BaseClient


class CityClient(BaseClient):
    """HTTP client for city-service's JSON API."""

    async def list_all(self) -> list[dict]:
        return await self._get("/cities")

    async def find(self, id: int) -> dict | None:
        return await self._get(f"/cities/{id}") 

    async def add(self, name: str) -> dict:
        return await self._post("/cities", {"name": name})

    async def update(self, id: int, name: str) -> dict:
        return await self._put(f"/cities/{id}", {"name": name})

    async def delete(self, id: int) -> None:
        await self._delete(f"/cities/{id}")
