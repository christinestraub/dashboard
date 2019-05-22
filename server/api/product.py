from flask_restful import Resource
from server.loumidis_db import select_product_name, select_product_type

class ProductRes(Resource):
    def __init__(self, **kwargs):
        pass

    def get(self, field_name):
        try:
            if field_name == 'name':
                records = select_product_name()
            elif field_name == 'type':
                records = select_product_type()
            else:
                return []

            print(records)

            return records

        except Exception as e:
            return '{}'.format(e), 400