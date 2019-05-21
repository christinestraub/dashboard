import pandas
from server.loumidis_db import insert_data

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_csv(connection, filepath):
    row_count = 0
    df = pandas.read_csv(filepath)
    print(len(df))

    for index, row in df.iterrows():
        # print(index, row['MCGS_Time'], row['MCGS_TIMEMS'], row['Weight_g'])
        try:
            data = (row['MCGS_Time'], str(row['MCGS_TIMEMS']), str(row['Weight_g']), row['Product_name'], row['Product_type'])
            insert_data(connection, data)
            row_count = row_count + 1
        except Exception as e:
            print(e)

    return row_count
