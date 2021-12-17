from app.exc import DataNotFound, UnauthorizedAccessError
from app.models.address_model import AddressModel
from flask_restful import reqparse
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from http import HTTPStatus
from app.models.users_model import UserModel
from app.services.helper import BaseServices


class AddressService(BaseServices):
    model = AddressModel


    @staticmethod
    def create() -> AddressModel:
        user_logged = get_jwt_identity()

        parser = reqparse.RequestParser()

        parser.add_argument("zip_code", type=str, required=True)
        parser.add_argument("address", type=str, required=True)
        parser.add_argument("number", type=str, required=True)
        parser.add_argument("city", type=str, required=True)
        parser.add_argument("state", type=str, required=True)
        parser.add_argument("country", type=str, required=True)

        data = parser.parse_args(strict=True)

        data['user_id'] = user_logged['id']
        
        new_address: AddressModel = AddressModel(**data)
        new_address.save()

        return jsonify(new_address), HTTPStatus.CREATED


    @staticmethod
    def update(address_id) -> AddressModel:
        user_logged = get_jwt_identity()

        address = AddressModel.query.get(address_id)
        if not address:
            raise DataNotFound('Address')

        if address.user_id != user_logged['id'] and user_logged['user_role'] == 'user':
            raise UnauthorizedAccessError

        parser = reqparse.RequestParser()

        parser.add_argument("zip_code", type=str, store_missing=False)
        parser.add_argument("address", type=str, store_missing=False)
        parser.add_argument("number", type=str, store_missing=False)
        parser.add_argument("city", type=str, store_missing=False)
        parser.add_argument("state", type=str, store_missing=False)
        parser.add_argument("country", type=str, store_missing=False)

        data = parser.parse_args(strict=True)

        for key, value in data.items():
            setattr(address, key, value)
        
        address.save()

        return jsonify(address), HTTPStatus.OK


    @staticmethod
    def get_by_id(address_id) -> AddressModel:
        user_logged = get_jwt_identity()

        address: AddressModel = AddressModel.query.get(address_id)
        if not address:
            raise DataNotFound('Address')

        if address.user_id != user_logged['id'] and user_logged['user_role'] == 'user':
            raise UnauthorizedAccessError

        return jsonify(address), HTTPStatus.OK


    @staticmethod
    def get_my_addresses():
        user_logged = get_jwt_identity()
        
        user_found: UserModel = UserModel.query.get(user_logged['id'])

        if not user_found:
            raise DataNotFound('User')

        return jsonify(user_found.addresses), HTTPStatus.OK

    
    @staticmethod
    def delete(address_id) -> AddressModel:
        user_logged = get_jwt_identity()

        address: AddressModel = AddressModel.query.get(address_id)
        if not address:
            raise DataNotFound('Address')

        if address.user_id != user_logged['id'] and user_logged['user_role'] == 'user':
            raise UnauthorizedAccessError

        address.delete()

        return '', HTTPStatus.NO_CONTENT
