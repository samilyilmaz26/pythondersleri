import os

from flask import Flask, jsonify, request

from models.department import Department
from repo.department_repository import DepartmentRepository


class DepartmentServiceApp:
    """JSON REST API for the Bolum (department) table."""

    def __init__(self, db_path=None, port=None):
        self.app = Flask(__name__)
        self.port = port or int(os.environ.get("PORT", 5002))
        self.repo = DepartmentRepository(db_path or os.environ.get("DB_PATH", "departments.db"))
        self._register_routes()

    def _register_routes(self):
        app = self.app
        app.add_url_rule("/health", "health", self.health)
        app.add_url_rule("/departments", "list_departments", self.list_departments, methods=["GET"])
        app.add_url_rule("/departments", "create_department", self.create_department, methods=["POST"])
        app.add_url_rule("/departments/<int:id>", "get_department", self.get_department, methods=["GET"])
        app.add_url_rule("/departments/<int:id>", "update_department", self.update_department, methods=["PUT"])
        app.add_url_rule("/departments/<int:id>", "delete_department", self.delete_department, methods=["DELETE"])

    def health(self):
        return jsonify({"status": "ok"})

    def list_departments(self):
        return jsonify([d.to_dict() for d in self.repo.list_all()])

    def get_department(self, id):
        department = self.repo.find(id)
        if department is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(department.to_dict())

    def create_department(self):
        data = request.get_json(force=True)
        department = Department(bolumad=data.get("bolumad"))
        department.id = self.repo.add(department)
        return jsonify(department.to_dict()), 201

    def update_department(self, id):
        data = request.get_json(force=True)
        department = Department(id=id, bolumad=data.get("bolumad"))
        self.repo.update(department)
        return jsonify(department.to_dict())

    def delete_department(self, id):
        self.repo.delete(id)
        return "", 204

    def run(self, debug=True):
        self.app.run(host="0.0.0.0", port=self.port, debug=debug)


if __name__ == "__main__":
    DepartmentServiceApp().run(debug=os.environ.get("FLASK_DEBUG", "1") == "1")
