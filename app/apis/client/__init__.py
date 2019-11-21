from flask_restful import Api
from app.apis.client.user_api import UsersResource
client_api = Api(prefix='/api/client')

client_api.add_resource(UsersResource,'/user/')