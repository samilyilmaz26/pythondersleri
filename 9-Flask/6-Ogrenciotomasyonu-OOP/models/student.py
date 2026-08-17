from models.base_model import BaseModel

class Student(BaseModel):
    """Represents a row of the Ogrenci table (a student)."""

    def __init__(self, id=None, ad="", soyad="", bolumid=None, bolumad=None,
                 mahalle="", cadde="", kapino="", city=""):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.bolumid = bolumid
        # bolumad (department name) is only present when the student was
        # loaded together with its department via a join query.
        self.bolumad = bolumad
        self.mahalle = mahalle
        self.cadde = cadde
        self.kapino = kapino
        self.city = city

    @property
    def full_name(self):
        return f"{self.ad} {self.soyad}"

    @classmethod
    def from_form(cls, form, id=None):
        return cls(
            id=id,
            ad=form.get("ad"),
            soyad=form.get("soyad"),
            bolumid=form.get("bolumid"),
            mahalle=form.get("mahalle"),
            cadde=form.get("cadde"),
            kapino=form.get("kapino"),
            city=form.get("city"),
        )
