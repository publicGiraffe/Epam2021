from app import db


class Place(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'address', name='_name_address_uc'), )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Place {self.id=}, {self.name=}>'
