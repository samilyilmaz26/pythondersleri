from clients.base_client import BaseClient


class TitleClient(BaseClient):
    """HTTP client for title-service's JSON API."""

    async def list_all(self) -> list[dict]:
        return await self._get("/titles")

    async def find(self, id: int) -> dict | None:
        return await self._get(f"/titles/{id}") 

    async def add(self, name: str) -> dict:
        return await self._post("/titles", {"name": name})

    async def update(self, id: int, name: str) -> dict:
        return await self._put(f"/titles/{id}", {"name": name})

    async def delete(self, id: int) -> None:
        await self._delete(f"/titles/{id}")
