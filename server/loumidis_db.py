import pymysql.cursors

# Connect to the database
def connect_db(host, user, password, db):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def insert_data(connection, data):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `tbl_data` (`mcgs_time`, `mcgs_timems`, `weight`, `product_name`, `product_type`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print(e)

def select_data(connection, sql):
    try:
        records = []
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            result = cursor.fetchall()

            # Converting data into list
            for row in result:
                records.append([
                    row['id'],
                    str(row['mcgs_time']),
                    row['mcgs_timems'],
                    row['weight'],
                    row['product_name'],
                    row['product_type']
                ])

        return records

    except Exception as e:
        print(e)
        return []
