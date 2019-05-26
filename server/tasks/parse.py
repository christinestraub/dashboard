import pandas
from server.loumidis_db import insert_data

def parse_csv(file_path):
    df = pandas.read_csv(file_path)

    try:
        row_count = 0
        for index, row in df.iterrows():
            data = (
                row['MCGS_Time'],
                str(row['MCGS_TIMEMS']),
                str(row['Weight_g']),
                row['Product_name'],
                row['Product_type']
            )
            insert_data(data)
            row_count = row_count + 1
        print('parse_csv: {}'.format(row_count))
        return row_count
    except Exception as e:
        print('parse_and_add: {}'.format(e))

    return -1
    