from clients.auth_client import AuthClient
from clients.department_client import DepartmentClient
from clients.title_client import TitleClient
from clients.student_client import StudentClient
from clients.instructor_client import InstructorClient
from clients.base_client import ServiceUnavailableError

__all__ = [
    "AuthClient",
    "DepartmentClient",
    "TitleClient",
    "StudentClient",
    "InstructorClient",
    "ServiceUnavailableError",
]
