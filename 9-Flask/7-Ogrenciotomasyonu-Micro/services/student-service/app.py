import os

from flask import Flask, jsonify, request

from models.student import Student
from repo.student_repository import StudentRepository


class StudentServiceApp:
    """JSON REST API for the Ogrenci (student) table.

    Stores bolumid only; it never calls department-service itself.
    Resolving bolumid to a department name is the gateway's job.
    """

    def __init__(self, db_path=None, port=None):
        self.app = Flask(__name__)
        self.port = port or int(os.environ.get("PORT", 5004))
        self.repo = StudentRepository(db_path or os.environ.get("DB_PATH", "students.db"))
        self._register_routes()

    def _register_routes(self):
        app = self.app
        app.add_url_rule("/health", "health", self.health)
        app.add_url_rule("/students", "list_students", self.list_students, methods=["GET"])
        app.add_url_rule("/students", "create_student", self.create_student, methods=["POST"])
        app.add_url_rule("/students/<int:id>", "get_student", self.get_student, methods=["GET"])
        app.add_url_rule("/students/<int:id>", "update_student", self.update_student, methods=["PUT"])
        app.add_url_rule("/students/<int:id>", "delete_student", self.delete_student, methods=["DELETE"])

    def health(self):
        return jsonify({"status": "ok"})

    def list_students(self):
        return jsonify([s.to_dict() for s in self.repo.list_all()])

    def get_student(self, id):
        student = self.repo.find(id)
        if student is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(student.to_dict())

    def _student_from_json(self, data, id=None):
        return Student(
            id=id,
            ad=data.get("ad"),
            soyad=data.get("soyad"),
            bolumid=data.get("bolumid"),
            mahalle=data.get("mahalle"),
            cadde=data.get("cadde"),
            kapino=data.get("kapino"),
            city=data.get("city"),
        )

    def create_student(self):
        student = self._student_from_json(request.get_json(force=True))
        student.id = self.repo.add(student)
        return jsonify(student.to_dict()), 201

    def update_student(self, id):
        student = self._student_from_json(request.get_json(force=True), id=id)
        self.repo.update(student)
        return jsonify(student.to_dict())

    def delete_student(self, id):
        self.repo.delete(id)
        return "", 204

    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


if __name__ == "__main__":
    StudentServiceApp().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
