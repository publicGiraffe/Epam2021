from collections.abc import Iterable
from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from app import api
from services import CategoryService

categories_ns = api.namespace('categories', description='Categories related operations')

category_model = api.model('Category', {
    'name': fields.String(required=True),
})


def to_json(category):
    try:
        if isinstance(category, Iterable):
            result = []
            for ctg in category:
                result.append({
                    'id': ctg.id,
                    'name': ctg.name,
                })
        else:
            result = {
                'id': category.id,
                'name': category.name,
            }
        return result
    except AttributeError:
        raise TypeError(f'Wrong type, expected: Iterable | Category, given {type(category).__name__}')


def result_wrapper(result: dict | str, status_code: int = 0):
    if isinstance(result, dict | str):
        response = jsonify(result)
    else:
        response = jsonify(to_json(result))
    if status_code:
        response.status_code = status_code
    return response


@categories_ns.route('/')
class CategoryListResource(Resource):
    @categories_ns.doc('Get all the Categories')
    def get(self):
        categories = CategoryService.get_by_filter()
        return result_wrapper(categories, 200)

    @categories_ns.expect(category_model)
    @categories_ns.doc('Create a Category')
    def post(self):
        category_json = request.get_json()
        response = CategoryService.insert(name=category_json['name'])
        if not response:
            return result_wrapper({'message': "Congrats! You have successfully added a new category!"}, 201)
        return result_wrapper({'error_message': str(response)}, 400)


@categories_ns.route('/<int:category_id>')
class CategoryResource(Resource):
    def get(self, category_id):
        category = CategoryService.get_by_id(category_id)
        if category:
            return result_wrapper(category, 200)
        return result_wrapper({'error_message': 'Category not found'}, 404)

    @categories_ns.expect(category_model)
    def patch(self, category_id):
        if not CategoryService.get_by_id(category_id):
            return result_wrapper({'error_message': 'Category not found'}, 404)
        response = CategoryService.update(category_id, name=request.json['name'])
        if response:
            return result_wrapper({'error_message': str(response)}, 400)
        category = CategoryService.get_by_id(category_id)
        return result_wrapper(category, 200)

    def delete(self, category_id):
        if not CategoryService.get_by_id(category_id):
            return result_wrapper({'error_message': 'Category not found'}, 404)
        response = CategoryService.delete(category_id)
        if response:
            return result_wrapper({'error_message': str(response)}, 400)
        return result_wrapper({'message': 'Farewell.'})
