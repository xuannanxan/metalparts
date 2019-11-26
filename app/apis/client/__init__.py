from flask_restful import Api
from app.apis.client.user import UsersResource
from app.apis import api_blueprint

client_api = Api(api_blueprint)

client_api.add_resource(UsersResource,'/user/')