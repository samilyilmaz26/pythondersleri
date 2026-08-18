import requests


class ServiceUnavailableError(Exception):
    """Raised when a backend microservice can't be reached or fails."""


class BaseClient:
    """Thin JSON HTTP client shared by every service client.

    A 404 is treated as "not found" (returns None), not a failure.
    Anything else that goes wrong (connection refused, timeout, 5xx)
    raises ServiceUnavailableError so the gateway can turn it into a
    friendly flash message instead of a stack trace.
    """

    def __init__(self, base_url, timeout=3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise ServiceUnavailableError(f"{url} isteğine ulaşılamadı: {exc}") from exc

        if response.status_code == 404:
            return None
        if response.status_code >= 500:
            raise ServiceUnavailableError(f"{url} sunucu hatası döndürdü: {response.status_code}")
        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def _get(self, path):
        return self._request("GET", path)

    def _post(self, path, json):
        return self._request("POST", path, json=json)

    def _put(self, path, json):
        return self._request("PUT", path, json=json)

    def _delete(self, path):
        return self._request("DELETE", path)
