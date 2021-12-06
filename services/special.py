from sqlalchemy import sql
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import Special


class SpecialService:
    @classmethod
    def get_by_id(cls, special_id):
        special = Special.query.get(special_id)
        return special

    @classmethod
    def get_by_filter(cls, **kwargs):
        filtered_specials = Special.filter(sql.and_(**kwargs))
        return filtered_specials

    @classmethod
    def insert(cls, name, price, place_id, category_id, /):
        special = Special(
            name=name,
            price=price,
            place_id=place_id,
            category_id=category_id
        )
        try:
            db.session.add(special)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def update(cls, special_id, **kwargs):
        try:
            special = SpecialService.get_by_id(special_id)
            for key, value in kwargs:
                setattr(special, key, value)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def delete(cls, special_id):
        try:
            special = SpecialService.get_by_id(special_id)
            db.session.delete(special)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex
