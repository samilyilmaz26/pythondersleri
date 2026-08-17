from models.base_model import BaseModel


class Instructor(BaseModel):
    """Represents a row of the Egitmen table (an instructor)."""

    def __init__(self, id=None, ad="", soyad="", bolumid=None, bolumad=None,
                 unvanid=None, unvanad=None, mahalle="", cadde="", kapino="", city=""):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.bolumid = bolumid
        # bolumad/unvanad are only present when the instructor was loaded
        # together with its department/title via a join query.
        self.bolumad = bolumad
        self.unvanid = unvanid
        self.unvanad = unvanad
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
            unvanid=form.get("unvanid"),
            mahalle=form.get("mahalle"),
            cadde=form.get("cadde"),
            kapino=form.get("kapino"),
            city=form.get("city"),
        )
