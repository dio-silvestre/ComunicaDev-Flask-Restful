from flask import Flask
from flask_restful import Api


def init_app(app: Flask) -> None:
    api = Api(app)

    from app.models.leads_model import LeadModel
    from app.models.users_model import UserModel
    from app.models.categories_model import CategoryModel
    from app.models.lessons_model import LessonModel
    from app.models.user_token_model import UserTokenModel
    from app.models.user_lesson_model import UserLessonModel
    from app.models.captchas_model import CaptchaModel


    from app.views.address_view import AddressResource, AddressRetrieveResource
    api.add_resource(AddressResource, "/api/address", endpoint="ADDRESSES")
    api.add_resource(AddressRetrieveResource, "/api/address/<int:address_id>", endpoint="ADDRESS_ID")


    from app.views.leads_view import LeadResource, LeadRetrieveResource, LeadSendEmailResource
    api.add_resource(LeadResource, "/api/leads", endpoint="LEADS")
    api.add_resource(LeadRetrieveResource, "/api/leads/<int:lead_id>", endpoint="LEAD_ID")
    api.add_resource(LeadSendEmailResource, "/api/leads/newsletter", endpoint="LEADS_NEWSLETTER")


    from app.views.categories_view import CategoryResource, CategoryRetrieveResource
    api.add_resource(CategoryResource, "/api/categories", endpoint="CATEGORIES")
    api.add_resource(CategoryRetrieveResource, "/api/categories/<int:category_id>", endpoint="CATEGORY_ID")


    from app.views.users_view import UserResource, UserRetrieveResource, UserBasicResource, UserValidateTokenResource, UserLoginResource
    api.add_resource(UserResource, "/api/users", endpoint="USERS")
    api.add_resource(UserBasicResource, "/api/users/basic", endpoint="USERS_BASIC_NEW")
    api.add_resource(UserRetrieveResource, "/api/users/<int:user_id>", endpoint="USER_ID")
    api.add_resource(UserLoginResource, "/api/users/login", endpoint="USER_LOGIN")
    api.add_resource(UserValidateTokenResource, "/validate/<token>", endpoint="USER_VALIDATE_TOKEN")
