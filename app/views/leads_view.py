from http import HTTPStatus
from app.exc import DataAlreadyRegistered, DataNotFound, InvalidEmailError
from flask_restful import Resource
from flask import make_response
from flask_jwt_extended import jwt_required

from app.services.leads_service import LeadService
from app.configs.decorators import verify_role_admin


class LeadResource(Resource):

    @jwt_required()
    @verify_role_admin
    def get(self):
        return make_response(LeadService.get_all())


    def post(self):
        try:
            return make_response(LeadService.create())
        except InvalidEmailError as e:
            return {'error': e.message}, HTTPStatus.BAD_REQUEST
        except DataAlreadyRegistered as e:
            return {'error': e.message}, HTTPStatus.CONFLICT


class LeadRetrieveResource(Resource):

    @jwt_required()
    @verify_role_admin
    def get(self, lead_id):
        try:
            return make_response(LeadService.get_by_id(lead_id))
        except DataNotFound as e:
            return e.message, HTTPStatus.NOT_FOUND
    

    @jwt_required()
    @verify_role_admin
    def patch(self, lead_id):
        try:
            return make_response(LeadService.update(lead_id))
        except DataNotFound as e:
            return e.message, HTTPStatus.NOT_FOUND

    
    def delete(self, lead_id):
        try:
            return make_response(LeadService.delete(lead_id))
        except DataNotFound as e:
            return e.message, HTTPStatus.NOT_FOUND


class LeadSendEmailResource(Resource):
    
    @jwt_required()
    @verify_role_admin
    def post(self):
        return make_response(LeadService.newsletter_info())
