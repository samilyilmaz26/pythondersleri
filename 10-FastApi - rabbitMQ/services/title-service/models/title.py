from models.base_model import BaseModel


class Title(BaseModel):
    """Represents a row of the titles table."""

    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name
