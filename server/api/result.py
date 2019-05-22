import os
import json

from flask import request
from flask_restful import Resource
from server.loumidis_db import select_result


class ResultRes(Resource):
    def __init__(self, **kwargs):
        self.upload_folder = kwargs.get('upload_folder')

    def get(self, data_id):
        try:
            file_name = '{}_result.json'.format(data_id)
            file_path = os.path.join(self.upload_folder, file_name)

            with open(file_path, 'r') as infile:
                result = json.load(infile)

            return result

        except Exception as e:
            return '{}'.format(e), 400


class ResultListRes(Resource):
    def __init__(self, **kwargs):
        pass

    def get(self):
        records = select_result()

        return records
