import httpx


class ServiceUnavailableError(Exception):
    """Raised when a backend microservice can't be reached or fails unexpectedly."""


class BaseClient:
    """Thin async JSON HTTP client shared by every service client.

    A 404 is treated as "not found" (returns None), not a failure.
    Anything else that goes wrong (connection refused, timeout, 5xx)
    raises ServiceUnavailableError so the gateway can turn it into a
    friendly flash message instead of a stack trace.
    """

    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def _send(self, method: str, path: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                return await client.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise ServiceUnavailableError(f"{url} isteğine ulaşılamadı: {exc}") from exc

    async def _request(self, method: str, path: str, **kwargs):
        response = await self._send(method, path, **kwargs)
        if response.status_code == 404:
            return None
        if response.status_code >= 500:
            raise ServiceUnavailableError(f"{path} sunucu hatası döndürdü: {response.status_code}")
        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    async def _get(self, path):
        return await self._request("GET", path)

    async def _post(self, path, json):
        return await self._request("POST", path, json=json)

    async def _put(self, path, json):
        return await self._request("PUT", path, json=json)

    async def _delete(self, path):
        return await self._request("DELETE", path)
