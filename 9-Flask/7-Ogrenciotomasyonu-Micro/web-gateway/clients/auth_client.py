import requests

from clients.base_client import BaseClient, ServiceUnavailableError


class AuthClient(BaseClient):
    """HTTP client for auth-service's JSON API.

    login() needs different handling than the generic CRUD clients:
    a 401 there means "wrong credentials" (a normal outcome), not a
    service failure, so it can't just reuse BaseClient's
    raise_for_status()-based _post().
    """

    def login(self, username, password):
        url = f"{self.base_url}/auth/login"
        try:
            response = requests.post(
                url, json={"username": username, "password": password}, timeout=self.timeout
            )
        except requests.RequestException as exc:
            raise ServiceUnavailableError(f"{url} isteğine ulaşılamadı: {exc}") from exc

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            return None
        raise ServiceUnavailableError(f"{url} beklenmeyen durum kodu: {response.status_code}")

    def register(self, username, email, password):
        return self._post("/auth/register", {"username": username, "email": email, "password": password})
