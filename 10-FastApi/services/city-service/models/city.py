from models.base_model import BaseModel


class City(BaseModel):
    """Represents a row of the cities table."""

    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name
