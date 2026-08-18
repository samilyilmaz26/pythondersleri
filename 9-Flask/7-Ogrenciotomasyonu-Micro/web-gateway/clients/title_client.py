from clients.base_client import BaseClient


class TitleClient(BaseClient):
    """HTTP client for title-service's JSON API."""

    def list_all(self):
        return self._get("/titles")

    def find(self, id):
        return self._get(f"/titles/{id}")

    def add(self, unvanad):
        return self._post("/titles", {"unvanad": unvanad})

    def update(self, id, unvanad):
        return self._put(f"/titles/{id}", {"unvanad": unvanad})

    def delete(self, id):
        return self._delete(f"/titles/{id}")
