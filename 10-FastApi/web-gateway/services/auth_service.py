from starlette.requests import Request

from clients.auth_client import AuthClient


class NotLoggedInError(Exception):
    """Raised when a protected route is visited without an active session."""


class AuthService:
    """Handles login, registration and session state for the gateway.

    Session state (who is logged in, on this gateway) lives in the
    request's session; credential verification and user storage are
    delegated to user-service over HTTP via the injected AuthClient.
    """

    def __init__(self, auth_client: AuthClient):
        self.auth_client = auth_client

    async def attempt_login(self, request: Request, username: str, password: str) -> bool:
        user = await self.auth_client.login(username, password)
        if user:
            request.session["logged_in"] = True
            request.session["username"] = user["username"]
            return True
        return False

    def logout(self, request: Request):
        request.session.clear()

    async def register(self, username: str, email: str, password: str):
        await self.auth_client.register(username, email, password)

    def is_logged_in(self, request: Request) -> bool:
        return bool(request.session.get("logged_in"))

    def require_login(self, request: Request):
        """FastAPI dependency: raise NotLoggedInError if there's no active session."""
        if not self.is_logged_in(request):
            raise NotLoggedInError()
