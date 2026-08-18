import os

from flask import Flask, jsonify, request

from models.unvan import Unvan
from repo.unvan_repository import UnvanRepository


class TitleServiceApp:
    """JSON REST API for the Unvan (instructor title) table."""

    def __init__(self, db_path=None, port=None):
        self.app = Flask(__name__)
        self.port = port or int(os.environ.get("PORT", 5003))
        self.repo = UnvanRepository(db_path or os.environ.get("DB_PATH", "titles.db"))
        self._register_routes()

    def _register_routes(self):
        app = self.app
        app.add_url_rule("/health", "health", self.health)
        app.add_url_rule("/titles", "list_titles", self.list_titles, methods=["GET"])
        app.add_url_rule("/titles", "create_title", self.create_title, methods=["POST"])
        app.add_url_rule("/titles/<int:id>", "get_title", self.get_title, methods=["GET"])
        app.add_url_rule("/titles/<int:id>", "update_title", self.update_title, methods=["PUT"])
        app.add_url_rule("/titles/<int:id>", "delete_title", self.delete_title, methods=["DELETE"])

    def health(self):
        return jsonify({"status": "ok"})

    def list_titles(self):
        return jsonify([u.to_dict() for u in self.repo.list_all()])

    def get_title(self, id):
        unvan = self.repo.find(id)
        if unvan is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(unvan.to_dict())

    def create_title(self):
        data = request.get_json(force=True)
        unvan = Unvan(unvanad=data.get("unvanad"))
        unvan.id = self.repo.add(unvan)
        return jsonify(unvan.to_dict()), 201

    def update_title(self, id):
        data = request.get_json(force=True)
        unvan = Unvan(id=id, unvanad=data.get("unvanad"))
        self.repo.update(unvan)
        return jsonify(unvan.to_dict())

    def delete_title(self, id):
        self.repo.delete(id)
        return "", 204

    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


if __name__ == "__main__":
    TitleServiceApp().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
