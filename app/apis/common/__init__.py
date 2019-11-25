from flask_restful import Api
from app.apis import api_blueprint
from .captcha import CaptchaResource
common_api = Api(api_blueprint)

common_api.add_resource(CaptchaResource,'/captcha/')