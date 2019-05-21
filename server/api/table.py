import os
import csv
import json
from datetime import datetime

from flask import request
from flask_restful import Resource
from server.loumidis_db import select_data

class TableRes(Resource):
    def __init__(self, **kwargs):
        self.connection = kwargs.get('connection')

    def get(self):
        conditions = []
        start_date = request.args.get('start_date')
        if start_date is not None and start_date != '':
            conditions.append("mcgs_time >= '{}'".format(start_date))
        end_date = request.args.get('end_date')
        if start_date is not None and end_date != '':
            conditions.append("mcgs_time <= '{}'".format(end_date))
        product_type = request.args.get('product_type')
        if product_type is not None and product_type != '':
            conditions.append("product_type = '{}'".format(product_type))

        where = ' AND '.join(conditions)

        sql = 'SELECT * FROM tbl_data'
        if where != '':
            sql = sql + ' WHERE ' + where

        print(sql)

        records = select_data(self.connection, sql)

        return records
