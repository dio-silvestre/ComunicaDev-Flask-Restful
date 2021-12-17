from http import HTTPStatus
from app.exc import DataNotFound, UnauthorizedAccessError
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import make_response

from app.services.lessons_service import LessonService
from app.configs.decorators import verify_role_admin


class LessonResource(Resource):

    @jwt_required()
    @verify_role_admin
    def get(self):
        return make_response(LessonService.get_all())


    @jwt_required()
    @verify_role_admin
    def post(self):
        return make_response(LessonService.create())


class LessonRetrieveResource(Resource):

    @jwt_required()
    def get(self, lesson_id):
        try:
            return make_response(LessonService.get_by_id(lesson_id))
        except DataNotFound as e:
            return e.message, e.code
        except UnauthorizedAccessError as e:
            return e.message, e.code
    

    @jwt_required()
    @verify_role_admin
    def patch(self, lesson_id):
        try:
            return make_response(LessonService.update(lesson_id))
        except DataNotFound as e:
            return e.message, e.code

    
    @jwt_required()
    @verify_role_admin
    def delete(self, lesson_id):
        try:
            return make_response(LessonService.delete(lesson_id))
        except DataNotFound as e:
            return e.message, e.code


class LessonListByUserResource(Resource):

    @jwt_required()
    def get(self):
        try:
            return make_response(LessonService.list_my_lessons())
        except KeyError:
            return {'error': 'Invalid token.'}, HTTPStatus.UNAUTHORIZED
        except DataNotFound as e:
            return e.message, e.code


class LessonUpdateFinishedResource(Resource):

    @jwt_required()
    def patch(self, id):
        return make_response(LessonService.update_finished(id))
