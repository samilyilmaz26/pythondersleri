

import sqlite3
class Sehir:
    def __init__(self, id=None, ad=None):
        self.id = id
        self.ad = ad
    @classmethod
    def from_row(cls, row):
        """Creates a PersonelModel instance from a sqlite3.Row object."""
        return cls(
            id=row['id'] if 'id' in row.keys() else None,
            ad=row['ad'] if 'ad' in row.keys() else None,
        )
class sehirRepository:
     

    def get_all(self):

        """Fetches all rows and maps them to a list of PersonelModel objects."""
        con  = sqlite3.connect("Banka.db")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
            
        sorgu = 'SELECT * FROM sehir'
        sehirler_sql = cursor.execute(sorgu).fetchall()

        print(s for s in sehirler_sql)
        # Map every row dictionary into a PersonelModel object
        sehirlerx  =  [Sehir.from_row(row) for row in sehirler_sql]
        sehirler = []
        for s in sehirler_sql:
            sehirler.append(Sehir.from_row(s))
        return sehirler
# Inside your Flask views/controllers:def perlist():
    # repo = sehirRepository()
    # personel_objects = repo.get_all()  # Contains a list of PersonelModel instances
    # return render_template("personel/list.html", personel=personel_objects)

# The database columns are mapped directly into an explicit PersonelModel class. This encapsulates the data structure so your HTML templates can access properties using clean object syntax (e.g., {{ p.ad }} instead of {{ p['ad'] }}).
# If you want to expand this model, let me know if you would like to:

# * Add a save or update method to the model to handle inserts and edits directly.
# * Introduce a validation method inside the model to check if inputs like email or salary are formatted correctly.
# * See how to write the Jinja template code for this object-based list.


