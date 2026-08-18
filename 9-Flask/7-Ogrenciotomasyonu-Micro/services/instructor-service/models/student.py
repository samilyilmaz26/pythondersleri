from models.base_model import BaseModel

class Student(BaseModel):
    """Represents a row of the Ogrenci table (a student).

    Instructor reuses these fields via inheritance, exactly like the
    original monolith's models/student.py and models/instructor.py.
    This service never exposes a Student API itself — student-service
    owns that — it only needs the shared shape for Instructor.
    """

    def __init__(self, id=None, ad="", soyad="", bolumid=None, bolumad=None,
                 mahalle="", cadde="", kapino="", city=""):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.bolumid = bolumid
        self.bolumad = bolumad
        self.mahalle = mahalle
        self.cadde = cadde
        self.kapino = kapino
        self.city = city

    @property
    def full_name(self):
        return f"{self.ad} {self.soyad}"

    @property
    def full_address(self):
        parts = [self.mahalle, self.cadde, self.kapino, self.city]
        return " ".join(part for part in parts if part)
