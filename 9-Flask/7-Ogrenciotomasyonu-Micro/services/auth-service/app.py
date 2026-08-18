import os

from flask import Flask, jsonify, request
from passlib.hash import sha256_crypt

from repo.user_repository import UserRepository


class AuthServiceApp:
    """JSON REST API for the User table: registration and credential checks.

    Owns password hashing so no other service ever sees a plaintext
    password at rest; the web-gateway only forwards what the browser
    submitted and keeps the resulting session for itself.
    """

    def __init__(self, db_path=None, port=None):
        self.app = Flask(__name__)
        self.port = port or int(os.environ.get("PORT", 5001))
        self.repo = UserRepository(db_path or os.environ.get("DB_PATH", "users.db"))
        self._register_routes()

    def _register_routes(self):
        app = self.app
        app.add_url_rule("/health", "health", self.health)
        app.add_url_rule("/auth/login", "login", self.login, methods=["POST"])
        app.add_url_rule("/auth/register", "register", self.register, methods=["POST"])

    def health(self):
        return jsonify({"status": "ok"})

    def login(self):
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        user = self.repo.find_by_username(username)
        if user and sha256_crypt.verify(password, user.password):
            return jsonify({"id": user.id, "username": user.username, "email": user.email})
        return jsonify({"error": "invalid credentials"}), 401

    def register(self):
        data = request.get_json(force=True)
        hashed_password = sha256_crypt.encrypt(data.get("password"))
        new_id = self.repo.register(data.get("username"), data.get("email"), hashed_password)
        return jsonify({"id": new_id, "username": data.get("username"), "email": data.get("email")}), 201

    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


if __name__ == "__main__":
    AuthServiceApp().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
