from functools import wraps

from flask import session, flash, redirect, url_for
from passlib.hash import sha256_crypt

from repo.user_repository import UserRepository


class AuthService:
    """Handles login, registration and access control.

    Wraps a UserRepository so the rest of the application never
    touches passwords or sessions directly.
    """

    def __init__(self, user_repository=None):
        self.user_repository = user_repository or UserRepository()

    def attempt_login(self, username, password):
        """Try to log a user in. Returns True/False and sets the session."""
        user = self.user_repository.find_by_username(username)
        if user and sha256_crypt.verify(password, user.password):
            session["logged_in"] = True
            session["username"] = username
            return True
        return False

    def logout(self):
        session.clear()

    def register(self, username, email, password):
        hashed_password = sha256_crypt.encrypt(password)
        self.user_repository.register(username, email, hashed_password)

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
