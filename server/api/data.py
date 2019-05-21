import os
import csv
import json
from datetime import datetime

from flask import request
from flask_restful import Resource

from .proc import test_data

columns = ('MCGS_Time', 'MCGS_TIMEMS', 'Weight_g', 'Product_name', 'Product_type')

class DataRes(Resource):
    def __init__(self, **kwargs):
        self.upload_folder = kwargs.get('upload_folder')

    def get(self, data_id):
        try:
            file_name = '{}_result.json'.format(data_id)
            file_path = os.path.join(self.upload_folder, file_name)

            with open(file_path, 'r') as outfile:
                result = json.load(outfile)

            return result

        except Exception as e:
            return '{}'.format(e), 400

    def post(self, data_id):
        try:
            payload = request.json

            if 'filename' not in payload:
                return 'missing filename', 400
            if 'data' not in payload:
                return 'missing data', 400
            if 'options' not in payload:
                return 'missing options', 400

            filename = payload['filename']

            options = {
                'start_date': None,
                'end_date': None,
                'product_type': None,
                # 'batch_size': 100,
                # 'nominal_weight': 100
            }

            opt = payload['options']
            if 'start_date' in opt:
                if opt['start_date'] != '':
                    options['start_date'] = opt['start_date']
            if 'end_date' in opt:
                if opt['end_date'] != '':
                    options['end_date'] = opt['end_date']
            if 'product_type' in opt:
                options['product_type'] = opt['product_type']
            # if 'batch_size' in opt:
            #     options['batch_size'] = opt['batch_size']
            # if 'nominal_weight' in opt:
            #     options['nominal_weight'] = opt['nominal_weight']

            # store file to upload directory
            data_id = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]

            file_name = '{}_{}'.format(data_id, filename)
            file_path = os.path.join(self.upload_folder, file_name)

            with open(file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(columns)
                for row in payload['data']:
                    csv_writer.writerow(row)

            result = test_data(self.upload_folder, file_path, options, data_id)

            file_name = '{}_result.json'.format(data_id)
            file_path = os.path.join(self.upload_folder, file_name)

            with open(file_path, 'w') as outfile:
                json.dump(result, outfile)

            return { 'id': data_id }

        except Exception as e:
            return '{}'.format(e), 400
