import os

from flask import Flask, jsonify, request

from models.instructor import Instructor
from repo.instructor_repository import InstructorRepository


class InstructorServiceApp:
    """JSON REST API for the Egitmen (instructor) table.

    Stores bolumid/unvanid only; it never calls department-service or
    title-service itself. Resolving those ids to names is the
    gateway's job.
    """

    def __init__(self, db_path=None, port=None):
        self.app = Flask(__name__)
        self.port = port or int(os.environ.get("PORT", 5005))
        self.repo = InstructorRepository(db_path or os.environ.get("DB_PATH", "instructors.db"))
        self._register_routes()

    def _register_routes(self):
        app = self.app
        app.add_url_rule("/health", "health", self.health)
        app.add_url_rule("/instructors", "list_instructors", self.list_instructors, methods=["GET"])
        app.add_url_rule("/instructors", "create_instructor", self.create_instructor, methods=["POST"])
        app.add_url_rule("/instructors/<int:id>", "get_instructor", self.get_instructor, methods=["GET"])
        app.add_url_rule("/instructors/<int:id>", "update_instructor", self.update_instructor, methods=["PUT"])
        app.add_url_rule("/instructors/<int:id>", "delete_instructor", self.delete_instructor, methods=["DELETE"])

    def health(self):
        return jsonify({"status": "ok"})

    def list_instructors(self):
        return jsonify([i.to_dict() for i in self.repo.list_all()])

    def get_instructor(self, id):
        instructor = self.repo.find(id)
        if instructor is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(instructor.to_dict())

    def _instructor_from_json(self, data, id=None):
        return Instructor(
            id=id,
            ad=data.get("ad"),
            soyad=data.get("soyad"),
            bolumid=data.get("bolumid"),
            mahalle=data.get("mahalle"),
            cadde=data.get("cadde"),
            kapino=data.get("kapino"),
            city=data.get("city"),
            unvanid=data.get("unvanid"),
        )

    def create_instructor(self):
        instructor = self._instructor_from_json(request.get_json(force=True))
        instructor.id = self.repo.add(instructor)
        return jsonify(instructor.to_dict()), 201

    def update_instructor(self, id):
        instructor = self._instructor_from_json(request.get_json(force=True), id=id)
        self.repo.update(instructor)
        return jsonify(instructor.to_dict())

    def delete_instructor(self, id):
        self.repo.delete(id)
        return "", 204

    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


if __name__ == "__main__":
    InstructorServiceApp().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
