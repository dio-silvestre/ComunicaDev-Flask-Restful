from app.exc import DataNotFound
from app.models.captchas_model import CaptchaModel
from flask_restful import reqparse
from flask import jsonify
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from app.services.helper import BaseServices
from app.services.generate_image_captcha import generate_image_captcha
from app.models.captchas_model import CaptchaModel


class CaptchaService(BaseServices):
    model = CaptchaModel


    @staticmethod
    def generate_captcha() -> CaptchaModel:

        captcha_content, url_captcha = generate_image_captcha(6)

        new_captcha = CaptchaModel(captcha_content=captcha_content, url_captcha=url_captcha)

        new_captcha.save()
            
        return jsonify(new_captcha), HTTPStatus.CREATED


    @staticmethod
    def validate_captcha() -> CaptchaModel:

        parser = reqparse.RequestParser()

        parser.add_argument("url_captcha", type=str, store_missing=True)
        parser.add_argument("input_user", type=str, store_missing=True)

        data = parser.parse_args(strict=True)

        url_captcha = data["url_captcha"]
        input_user = data["input_user"]

        found_captcha: CaptchaModel = CaptchaModel.query.filter_by(url_captcha=url_captcha).first()
        
        if not found_captcha:
            raise DataNotFound('Captcha')

        if input_user == found_captcha.captcha_content:
            access_token = create_access_token(found_captcha)

            found_captcha.delete()

            return jsonify({"access_token": access_token}), HTTPStatus.OK

        return jsonify({"error": "Not authorized."}), HTTPStatus.BAD_REQUEST

