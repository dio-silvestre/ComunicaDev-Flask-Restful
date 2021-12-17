from app.exc import DataNotFound
from app.models.lessons_model import LessonModel
from app.models.users_model import UserModel
from app.models.categories_model import CategoryModel
from app.models.user_lesson_model import UserLessonModel
from flask_restful import reqparse
from flask import jsonify
from http import HTTPStatus
from app.services.helper import BaseServices
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.sql.elements import and_
from app.exc import UnauthorizedAccessError


class LessonService(BaseServices):
    model = LessonModel


    @staticmethod
    def create() -> LessonModel:
        parser = reqparse.RequestParser()

        parser.add_argument("title", type=str, required=True)
        parser.add_argument("description", type=str, required=True)
        parser.add_argument("url_video", type=str, required=True)
        parser.add_argument("is_premium", type=bool, required=True)
        parser.add_argument("category", type=str, required=True)

        data = parser.parse_args(strict=True)

        category_type = data.pop('category')

        category_found = CategoryModel.query.filter_by(type=category_type).first()

        if not category_found:
            new_category = CategoryModel(type=category_type, description="")
            new_category.save()

        category_found = CategoryModel.query.filter_by(type=category_type).first()

        new_lesson = LessonModel(category_id=category_found.id, **data)
        new_lesson.save()

        return jsonify(new_lesson), HTTPStatus.CREATED


    @staticmethod
    def update(lesson_id) -> LessonModel:
        lesson = LessonModel.query.get(lesson_id)
        if not lesson:
            raise DataNotFound('Lesson')

        parser = reqparse.RequestParser()

        parser.add_argument("title", type=str, store_missing=False)
        parser.add_argument("description", type=str, store_missing=False)
        parser.add_argument("url_video", type=str, store_missing=False)
        parser.add_argument("is_premium", type=bool, store_missing=False)
        parser.add_argument("category", type=str, store_missing=False)

        data = parser.parse_args(strict=True)

        if 'category' in data.keys():
            category_type = data.pop('category')

            category_found = CategoryModel.query.filter_by(type=category_type).first()

            if not category_found:
                new_category = CategoryModel(type=category_type, description="")
                new_category.save()

            category_found = CategoryModel.query.filter_by(type=category_type).first()

            data['category_id'] = category_found.id


        for key, value in data.items():
            setattr(lesson, key, value)
        
        lesson.save()
        return jsonify(lesson), HTTPStatus.OK


    @staticmethod
    def get_lesson_by_id(id: int):
        user_logged = get_jwt_identity()

        lesson: LessonModel = LessonModel.query.get(id)

        if not user_logged['is_premium'] and lesson.is_premium:
            raise UnauthorizedAccessError

        if not lesson:
            return {'error': 'Lesson does not exist'}, HTTPStatus.NOT_FOUND

        return jsonify(lesson), HTTPStatus.OK


    @staticmethod
    def list_my_lessons():
        user_logged = get_jwt_identity()

        user_lesson: UserLessonModel = UserLessonModel.query.filter_by(user_id=user_logged['id']).all()

        if not user_lesson:
            raise DataNotFound('Lessons')

        return jsonify(user_lesson), HTTPStatus.OK


    @staticmethod
    def update_finished(id):
        user = get_jwt_identity()
        user_lesson = UserLessonModel.query.filter(
                and_(UserLessonModel.lesson_id==id, UserLessonModel.user_id==user['id'])
            ).first()
        
        if not user_lesson:
            return {"error": "User and lesson don't match!"}, HTTPStatus.NOT_FOUND

        setattr(user_lesson, 'finished', True)

        user_lesson.save()
        
        user_lesson_updated = UserLessonModel.query.filter(
                and_(UserLessonModel.lesson_id==id, UserLessonModel.user_id==user['id'])
            ).first()

        return jsonify(user_lesson_updated), HTTPStatus.OK
