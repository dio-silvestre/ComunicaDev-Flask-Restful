from sqlalchemy.sql.elements import and_
from app.exc import DataNotFound, DataAlreadyRegistered, InvalidPassword, EmailVerifiedError, UnauthorizedAccessError, InvalidKey
from app.models.users_model import UserModel
from app.models.user_token_model import UserTokenModel
from app.models.lessons_model import LessonModel
from flask_restful import reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from http import HTTPStatus
from uuid import uuid4
from app.services.verify_user_email import verify_user_email
from app.services.helper import BaseServices
from app.services.reset_password import send_reset_password_code


class UserService(BaseServices):
    model = UserModel


    @staticmethod
    def create() -> UserModel:
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("cpf", type=str, required=True)
        parser.add_argument("password", type=str, required=True)

        data = parser.parse_args(strict=True)

        user_check = UserModel.query.filter_by(cpf=data.cpf).first()
        if user_check:
            raise DataAlreadyRegistered('CPF')
        
        user_check = UserModel.query.filter_by(email=data.email).first()
        if user_check:
            raise DataAlreadyRegistered('Email')

        if 'user_role' in data.keys():
            raise InvalidKey('user_role') 

        new_user: UserModel = UserModel(**data)
        new_user.save()

        access_token = create_access_token(new_user, expires_delta=timedelta(minutes=30))

        found_user = UserModel.query.filter_by(email=new_user.email).first()

        if found_user:
            info_token = {
                "user_id": found_user.id,
                "token": access_token,
                "token_expire": datetime.today()
            }
        else:
            return {'error': 'Failed to find user on database.'}, HTTPStatus.NOT_FOUND

        new_user_token: UserTokenModel = UserTokenModel(**info_token)

        new_user_token.save()

        verify_user_email(new_user.name, new_user.email, access_token)

        return jsonify(new_user), HTTPStatus.CREATED


    @staticmethod
    def get_my_data():
        user_logged = get_jwt_identity()

        found_user: UserModel = UserModel.query.filter_by(id=user_logged['id']).first()
        if not found_user:
            raise DataNotFound('User')
    
        return jsonify(found_user), HTTPStatus.OK


    @staticmethod
    def verify_user(token):
        token = UserTokenModel.query.filter_by(token=token).first()

        if token:
            user = UserModel.query.filter_by(id=token.user_id).first()
            setattr(user, 'verified', True)
            user.save()
            user_updated = UserModel.query.filter_by(id=token.user_id).first()

            return jsonify(user_updated), HTTPStatus.OK
        
        else:
            raise EmailVerifiedError        


    @staticmethod
    def user_login():
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, store_missing=True)
        parser.add_argument("password", type=str, store_missing=True)

        data = parser.parse_args(strict=True)

        email = data["email"]
        password = data["password"]

        found_user: UserModel = UserModel.query.filter_by(email=email).first()
        
        if not found_user:
            raise DataNotFound('User')

        if found_user.check_password(password):
            if found_user.is_premium:
                lessons = LessonModel.query.all()
            else:
                lessons = LessonModel.query.filter_by(is_premium=False).all()

            found_user.lessons = lessons

            found_user.save()

            access_token = create_access_token(identity=found_user)
            return {"token": access_token}, HTTPStatus.OK
        else:
            raise InvalidPassword


    @staticmethod
    def get_by_id(user_id):
        user_token = get_jwt_identity()

        if user_id != user_token['id']:
            raise UnauthorizedAccessError

        found_user: UserModel = UserModel.query.filter_by(id=user_id).first()

        if not found_user:
            raise DataNotFound('User')

        return jsonify(found_user), HTTPStatus.OK


    @staticmethod
    def update(user_id) -> UserModel:
        user_token = get_jwt_identity()

        if user_id != user_token['id']:
            raise UnauthorizedAccessError

        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, store_missing=False)
        parser.add_argument("name", type=str, store_missing=False)
        parser.add_argument("cpf", type=str, store_missing=False)
        parser.add_argument("password", type=str, store_missing=False)
        parser.add_argument("current_password", type=str, store_missing=True)

        data = parser.parse_args(strict=True)

        current_password = data.pop("current_password")

        updated_user: UserModel = UserModel.query.filter_by(id=user_id).first()

        if not updated_user:
            raise DataNotFound('User')

        updated_user.check_password(current_password)

        for key, value in data.items():
            setattr(updated_user, key, value)
        
        updated_user.save()
        return jsonify(updated_user), HTTPStatus.OK

    
    @staticmethod
    def delete(user_id) -> UserModel:
        user_logged = get_jwt_identity()

        if id != user_logged['id'] and user_logged['user_role'] == 'user':
            raise UnauthorizedAccessError

        user_to_delete : UserModel = UserModel.query.filter_by(id=user_id).first()

        if not user_to_delete:
            raise DataNotFound('User')

        user_to_delete.delete()

        return {'message': 'Successfully deleted.'}, HTTPStatus.OK


    @staticmethod
    def confirm_password_reset():
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, store_missing=True)

        data = parser.parse_args(strict=True)
    
        if 'email' in data:

            user = UserModel.query.filter_by(email=data['email']).first()

            if not user:
                raise DataNotFound('Email')

            reset_code = str(uuid4())[0:5]
            send_reset_password_code(user.name, user.email, reset_code)
            user_update = UserModel.query.filter_by(email=data['email']).first()
            setattr(user_update, 'reset_code', reset_code)
            
            user_update.save()

            return {'message': 'Mail sent to user successfully'}, HTTPStatus.OK


    @staticmethod
    def reset_user_password():        
        parser = reqparse.RequestParser()

        parser.add_argument("email", type=str, store_missing=True)
        parser.add_argument("reset_code", type=str, store_missing=True)
        parser.add_argument("new_password", type=str, store_missing=True)

        data = parser.parse_args(strict=True)

        user_to_update = UserModel.query.filter(and_(UserModel.reset_code==data['reset_code'], UserModel.email==data['email'])).first()

        if not user_to_update:
            raise DataNotFound('Reset code or email')

        setattr(user_to_update, 'password', data['new_password'])
        
        user_to_update.save()

        return {'message': 'User password reset successfully'}, HTTPStatus.OK