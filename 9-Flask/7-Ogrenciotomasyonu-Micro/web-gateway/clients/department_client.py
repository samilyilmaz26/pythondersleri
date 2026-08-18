from clients.base_client import BaseClient


class DepartmentClient(BaseClient):
    """HTTP client for department-service's JSON API."""

    def list_all(self):
        return self._get("/departments")

    def find(self, id):
        return self._get(f"/departments/{id}")

    def add(self, bolumad):
        return self._post("/departments", {"bolumad": bolumad})

    def update(self, id, bolumad):
        return self._put(f"/departments/{id}", {"bolumad": bolumad})

    def delete(self, id):
        return self._delete(f"/departments/{id}")
