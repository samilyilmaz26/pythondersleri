from models.base_model import BaseModel


class Department(BaseModel):
    """Represents a row of the department table."""

    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name
