from collections.abc import Iterable
from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from app import api
from services import PlaceService

places_ns = api.namespace('places', description='Places related operations')

place_model = api.model('Place', {
    'name': fields.String(required=True),
    'address': fields.String(required=True),
})


def to_json(place):
    try:
        if isinstance(place, Iterable):
            result = []
            for pl in place:
                result.append({
                    'id': pl.id,
                    'name': pl.name,
                    'address': pl.address,
                })
        else:
            result = {
                'id': place.id,
                'name': place.name,
                'address': place.address,
            }
        return result
    except AttributeError:
        raise TypeError(f'Wrong type, expected: Iterable | Place, given {type(place).__name__}')


def result_wrapper(result: dict | str, status_code: int = 0):
    if isinstance(result, dict | str):
        response = jsonify(result)
    else:
        response = jsonify(to_json(result))
    if status_code:
        response.status_code = status_code
    return response


@places_ns.route('/')
class PlaceListResource(Resource):
    @places_ns.doc('Get all the Places')
    def get(self):
        places = PlaceService.get_by_filter()
        return result_wrapper(places, 200)

    @places_ns.expect(place_model)
    @places_ns.doc('Create a Place')
    def post(self):
        place_json = request.get_json()
        response = PlaceService.insert(name=place_json['name'], address=place_json['address'])
        if not response:
            return result_wrapper({'message': "Congrats! You have successfully added a new place!"}, 201)
        return result_wrapper({'error_message': str(response)}, 400)


@places_ns.route('/<int:place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        place = PlaceService.get_by_id(place_id)
        if place:
            return result_wrapper(place, 200)
        return result_wrapper({'error_message': 'Place not found'}, 404)

    @places_ns.expect(place_model)
    def patch(self, place_id):
        if not PlaceService.get_by_id(place_id):
            return result_wrapper({'error_message': 'Place not found'}, 404)
        params = {}
        if 'name' in request.json:
            params['name'] = request.json['name']
        if 'address' in request.json:
            params['address'] = request.json['address']

        response = PlaceService.update(place_id, **params)
        if response:
            return result_wrapper({'error_message': str(response)}, 400)
        place = PlaceService.get_by_id(place_id)
        return result_wrapper(place, 200)

    def delete(self, place_id):
        if not PlaceService.get_by_id(place_id):
            return result_wrapper({'error_message': 'Place not found'}, 404)
        response = PlaceService.delete(place_id)
        if response:
            return result_wrapper({'error_message': str(response)}, 400)
        return result_wrapper({'message': 'Farewell.'})
