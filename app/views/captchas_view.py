from app.exc import DataNotFound
from flask_restful import Resource
from flask import make_response

from app.services.captchas_service import CaptchaService


class CaptchaGenerateResource(Resource):


    def get(self):
        return make_response(CaptchaService.generate_captcha())


class CaptchaValidateResource(Resource):
    

    def post(self):
        try:
            return make_response(CaptchaService.validate_captcha())
        except DataNotFound as e:
            return e.message, e.code
