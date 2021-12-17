from http import HTTPStatus
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import make_response

from app.exc import DataNotFound, InvalidZipCodeError, InvalidDataTypeError, UnauthorizedAccessError
from app.services.address_service import AddressService
from app.configs.decorators import verify_role_admin


class AddressResource(Resource):

    @jwt_required()
    @verify_role_admin
    def get(self):
        return make_response(AddressService.get_all())


    @jwt_required()
    def post(self):
        try:
            return make_response(AddressService.create())
        except InvalidDataTypeError as e:
            return e.message, e.code
        except InvalidZipCodeError as e:
            return e.message, e.code
        except KeyError:
            return {"error": "Invalid token."}, HTTPStatus.UNAUTHORIZED


class AddressRetrieveResource(Resource):

    @jwt_required()
    def get(self, address_id):
        try:
            return make_response(AddressService.get_by_id(address_id))
        except DataNotFound as e:
            return e.message, e.code
        except KeyError:
            return {'error': 'Invalid token.'}, HTTPStatus.UNAUTHORIZED
        except UnauthorizedAccessError as e:
            return e.message, e.code


    @jwt_required()
    def patch(self, address_id):
        try:
            return make_response(AddressService.update(address_id))
        except DataNotFound as e:
            return e.message, e.code
        except KeyError:
            return {'error': 'Invalid token.'}, HTTPStatus.UNAUTHORIZED
        except UnauthorizedAccessError as e:
            return e.message, e.code

    
    @jwt_required()
    def delete(self, address_id):
        try:
            return make_response(AddressService.delete(address_id))
        except DataNotFound as e:
            return e.message, e.code
        except KeyError:
            return {'error': 'Invalid token.'}, HTTPStatus.UNAUTHORIZED
        except UnauthorizedAccessError as e:
            return e.message, e.code


class AddressPersonalResource(Resource):

    @jwt_required()
    def get(self):
        try:
            return make_response(AddressService.get_my_addresses())
        except DataNotFound as e:
            return e.message, e.code
        except KeyError:
            return {'error': 'Invalid token.'}, HTTPStatus.UNAUTHORIZED
        except UnauthorizedAccessError as e:
            return e.message, e.code