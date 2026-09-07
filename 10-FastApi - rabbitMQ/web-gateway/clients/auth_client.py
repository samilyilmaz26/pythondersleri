from clients.base_client import BaseClient, ServiceUnavailableError


class UsernameTakenError(Exception):
    """Raised when registration is attempted with a username that already exists."""


class AuthClient(BaseClient):
    """HTTP client for user-service's JSON API.

    login() needs different handling than a generic POST: a 401 there
    means "wrong credentials" (a normal outcome), not a service
    failure. Likewise a 409 on register() means "username taken", not
    a failure.
    """

    async def login(self, username: str, password: str) -> dict | None:
        response = await self._send(
            "POST", "/auth/login", json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            return None
        raise ServiceUnavailableError(f"/auth/login beklenmeyen durum kodu: {response.status_code}")

    async def register(self, username: str, email: str, password: str) -> dict:
        response = await self._send(
            "POST", "/auth/register", json={"username": username, "email": email, "password": password}
        )
        if response.status_code == 201:
            return response.json()
        if response.status_code == 409:
            raise UsernameTakenError(username)
        raise ServiceUnavailableError(f"/auth/register beklenmeyen durum kodu: {response.status_code}")
