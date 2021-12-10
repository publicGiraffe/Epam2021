from sqlalchemy import sql
from sqlalchemy.exc import SQLAlchemyError

from app import db
from models import Category


class CategoryService:
    @classmethod
    def get_by_id(cls, category_id):
        category = Category.query.get(category_id)
        return category

    @classmethod
    def get_by_filter(cls, **kwargs):
        filtered_categories = Category.query.filter(sql.and_(**kwargs)).all()
        return filtered_categories

    @classmethod
    def insert(cls, name):
        category = Category(
            name=name
        )
        try:
            db.session.add(category)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def update(cls, category_id, **kwargs):
        try:
            category = CategoryService.get_by_id(category_id)
            for key, value in kwargs.items():
                setattr(category, key, value)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex

    @classmethod
    def delete(cls, category_id):
        try:
            category = CategoryService.get_by_id(category_id)
            db.session.delete(category)
            db.session.commit()
            return
        except SQLAlchemyError as ex:
            return ex
