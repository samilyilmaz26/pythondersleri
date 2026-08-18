from models.base_model import BaseModel

class Student(BaseModel):
    """View-model rebuilt from student-service's JSON responses.

    Kept here (not just raw dicts) so templates can still use
    full_name/full_address the way they did against the old ORM-ish
    model objects — a plain dict has no properties for Jinja to call.
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
