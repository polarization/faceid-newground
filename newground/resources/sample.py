# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

sample_bp = Blueprint('api', __name__)

sample_api = Api(sample_bp)


class Log(Resource):
    def get(self, id):
        return jsonify({'result': True})


sample_api.add_resource(Log, '/logs/<int:id>')
