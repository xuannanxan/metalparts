from flask_restful import Api
from app.apis.client.hello_api import Hello
client_api = Api(prefix='/client')

client_api.add_resource(Hello,'/hello/')