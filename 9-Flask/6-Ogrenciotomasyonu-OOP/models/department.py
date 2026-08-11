from models.base_model import BaseModel


class Department(BaseModel):
    """Represents a row of the Bolum table (a department)."""

    def __init__(self, id=None, bolumad=""):
        self.id = id
        self.bolumad = bolumad
