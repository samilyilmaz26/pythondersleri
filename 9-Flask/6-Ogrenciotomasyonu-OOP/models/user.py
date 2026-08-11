from models.base_model import BaseModel


class User(BaseModel):
    """Represents a row of the User table."""

    def __init__(self, id=None, username="", email="", password=""):
        self.id = id
        self.username = username
        self.email = email
        # Stored password hash (never a plaintext password).
        self.password = password
