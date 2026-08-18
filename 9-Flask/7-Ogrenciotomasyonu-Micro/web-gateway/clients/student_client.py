from clients.base_client import BaseClient


class StudentClient(BaseClient):
    """HTTP client for student-service's JSON API."""

    def list_all(self):
        return self._get("/students")

    def find(self, id):
        return self._get(f"/students/{id}")

    def add(self, data):
        return self._post("/students", data)

    def update(self, id, data):
        return self._put(f"/students/{id}", data)

    def delete(self, id):
        return self._delete(f"/students/{id}")
