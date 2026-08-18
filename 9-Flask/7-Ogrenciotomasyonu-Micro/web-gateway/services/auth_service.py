from functools import wraps

from flask import session, flash, redirect, url_for


class AuthService:
    """Handles login, registration and access control.

    Session state (who is logged in, on this gateway) lives here as
    before; credential verification and user storage are delegated to
    auth-service over HTTP via the injected AuthClient.
    """

    def __init__(self, auth_client):
        self.auth_client = auth_client

    def attempt_login(self, username, password):
        """Try to log a user in. Returns True/False and sets the session."""
        user = self.auth_client.login(username, password)
        if user:
            session["logged_in"] = True
            session["username"] = username
            return True
        return False

    def logout(self):
        session.clear()

    def register(self, username, email, password):
        self.auth_client.register(username, email, password)

    def is_logged_in(self):
        return "logged_in" in session

    def login_required(self, view_func):
        """Decorator: redirect to the login page if not authenticated."""

        @wraps(view_func)
        def decorated(*args, **kwargs):
            if self.is_logged_in():
                return view_func(*args, **kwargs)
            flash("Bu sayfaya gitmek için giriş yapmalısınız", "danger")
            return redirect(url_for("login"))

        return decorated
