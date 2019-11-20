from app.apis.client import client_api
from app.apis.admin import admin_api
from app.apis.company import company_api

def init_api(app):
    client_api.init_app(app)
    company_api.init_app(app)
    admin_api.init_app(app)