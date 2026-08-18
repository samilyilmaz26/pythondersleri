from clients.base_client import BaseClient


class InstructorClient(BaseClient):
    """HTTP client for instructor-service's JSON API."""

    def list_all(self):
        return self._get("/instructors")

    def find(self, id):
        return self._get(f"/instructors/{id}")

    def add(self, data):
        return self._post("/instructors", data)

    def update(self, id, data):
        return self._put(f"/instructors/{id}", data)

    def delete(self, id):
        return self._delete(f"/instructors/{id}")
