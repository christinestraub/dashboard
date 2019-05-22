import os
import pymysql.cursors
from datetime import datetime

DB_HOST = os.environ.get('DB_HOST', default='localhost')
DB_USER = os.environ.get('DB_USER', default='root')
DB_PASS = os.environ.get('DB_PASS', default='')
DB_NAME = os.environ.get('DB_NAME', default='loumidis')

# Connect to the database
def connect_db(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def insert_data(data):
    connection = connect_db()
    sql = "INSERT INTO `tbl_data` (`mcgs_time`, `mcgs_timems`, `weight`, `product_name`, `product_type`) VALUES (%s, %s, %s, %s, %s)"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4]))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()

def select_result():
    connection = connect_db()
    records = []
    sql = 'SELECT * FROM tbl_result;'
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            result = cursor.fetchall()

            # Converting data into list
            for row in result:
                records.append([
                    row['id'],
                    row['data_id'],
                    str(row['created_at']),
                    str(row['updated_at'])
                ])
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()

    return records


def insert_result(data_id):
    connection = connect_db()
    sql = "INSERT INTO `tbl_result` (`data_id`, `updated_at`) VALUES (%s, %s)"
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql, (data_id, updated_at))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()



def update_result(data_id):
    connection = connect_db()
    sql = "UPDATE `tbl_result` SET `updated_at` = %s WHERE `data_id` = %s"
    updated_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql, (updated_at, data_id))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()


def delete_result(data_id):
    connection = connect_db()
    sql = "DELETE FROM `tbl_result` WHERE `data_id` = %s"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql, data_id)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()


def select_data(sql):
    connection = connect_db()
    records = []
    try:
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
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()

    return records

def select_product_name():
    connection = connect_db()
    sql = 'SELECT product_name FROM tbl_data GROUP BY product_name ORDER BY product_name ASC;'
    records = []
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            result = cursor.fetchall()

            # Converting data into list
            for row in result:
                records.append(row['product_name'])
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()

    return records

def select_product_type():
    connection = connect_db()
    sql = 'SELECT product_type FROM tbl_data GROUP BY product_type ORDER BY product_type ASC;'
    records = []
    try:
        with connection.cursor() as cursor:
            # Create a new record
            cursor.execute(sql)
            result = cursor.fetchall()

            # Converting data into list
            for row in result:
                records.append(row['product_type'])
    except Exception as e:
        print('{}'.format(e))
    finally:
        connection.close()

    return records
