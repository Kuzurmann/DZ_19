from flask import request
from flask_restx import Resource, Namespace

from implemented import user_service

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    def post(self):
        req_json = request.json
        user_service.create_user(req_json)
        return '', 201
