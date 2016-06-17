# coding=utf-8
from flask import Blueprint
from flask_restful import Resource, Api, reqparse
import werkzeug
from newground.common import swift as swift
from newground.common import redis_cli as redis
import uuid
import datetime
import json
from config import FDBInfo_rediskeyname

bsb = Blueprint('biological_specificity_base', __name__)
bsb_api = Api(bsb)


class FDBShowDetail(Resource):

    def get(self, fdbname):
        pass


class FDBUpdate(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('newfdbname')

    def post(self, fdbname):
        args = self.parser.parse_args()
        fdbinfo = json.loads(redis.get_value(FDBInfo_rediskeyname))
        try:
            fdbinfo[args['newfdbname']] = fdbinfo[fdbname]
        except:
            return {"result": "fail", 'error': 'fdb not exists'}
        del fdbinfo[fdbname]
        if redis.set_keyvalue(FDBInfo_rediskeyname, json.dumps(fdbinfo)):
            return {"result": "success"}
        else:
            return {"result": "fail", 'error': 'failed to update fdb name'}


class LiveSampleCreate(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('fdbname')
    parser.add_argument('samplefile',
                        type=werkzeug.datastructures.FileStorage,
                        location='files')

    def post(self):
        args = self.parser.parse_args()
        fdbinfo = json.loads(redis.get_value(FDBInfo_rediskeyname))
        if args['fdbname'] not in fdbinfo:
            return {"result": "fail", 'error': 'fdb not exists'}

        today = str(datetime.date.today())
        swift_conn = swift.get_conn(args['fdbname'])
        if type(swift_conn) == 'dict' and 'error' in swift_conn:
            return swift_conn

        if swift.get_containerinfo(swift_conn, today) is None:
            today = str(datetime.date.today())
            swift.create_container(swift_conn, today)

        file_name = today + '_' + str(uuid.uuid1())
        if swift.create_object(swift_conn, today, file_name,
                               args['samplefile']):
            return {"result": "success", "file_name": file_name}
        else:
            return {"result": "fail"}


bsb_api.add_resource(FDBShowDetail, '/fdb/<fdbname>/showdetail')
bsb_api.add_resource(FDBUpdate, '/fdb/<fdbname>/update')
bsb_api.add_resource(LiveSampleCreate, '/livesample/create')
