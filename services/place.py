from sqlalchemy import sql
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import Place


class PlaceService:
    @classmethod
    def get_by_id(cls, place_id):
        place = Place.query.get(place_id)
        return place

    @classmethod
    def get_by_filter(cls, **kwargs):
        filtered_places = Place.query.filter(sql.and_(**kwargs)).all()
        return filtered_places

    @classmethod
    def insert(cls, name, address):
        place = Place(
            name=name,
            address=address
        )
        try:
            db.session.add(place)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def update(cls, place_id, **kwargs):
        try:
            place = PlaceService.get_by_id(place_id)
            for key, value in kwargs.items():
                setattr(place, key, value)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def delete(cls, place_id):
        try:
            place = PlaceService.get_by_id(place_id)
            db.session.delete(place)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex
