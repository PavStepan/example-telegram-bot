from datetime import datetime
import psycopg2
from config import get_db_config
from utils import check_data


def add_userdata_in_db(user_data, table_name):
    values = ""
    for value in user_data.values():
        values += "{},".format(check_data(value))
    values = values[:-1]
    user_query = "INSERT INTO SomeTable.{}({}) Values ({});".format(table_name, ",".join(list(user_data.keys())), values)
    _ = execute_query(user_query)


def add_gift_link(user_id, giver_id):
    if user_id == giver_id:
        return
    sql_query = f"SELECT presentDate, FROM SomeTable.Presents " \
                f"WHERE giverId = {giver_id} AND isApply = 1 AND userid = 0;"
    result = execute_query(sql_query)
    # gift_SMART_12
    if len(result) > 0:
        present_date = result[0][0]

        sql_query = f"UPDATE SomeTable.Presents SET userid={user_id} " \
                    f"WHERE giverId={int(giver_id)} AND isApply=1 AND presentDate='{present_date}';"
        _ = execute_query(sql_query)


def add_referral_link(user_id, reflink):
    sql_query = f"SELECT userId, referralTraffic from SomeTable.Users WHERE referralLink = '{reflink}';"
    result = execute_query(sql_query)
    if len(result) > 0 and result[0][0] != user_id:
        sql_query = f"UPDATE SomeTable.Users SET bonus = 1 where userId = {user_id}"
        _ = execute_query(sql_query)

        sql_query = f"INSERT INTO SomeTable.Referral(userId, giverLink, isApply, referralDate) " \
                    f"Values ({user_id},'{reflink}', 0, '{str(datetime.now())}');"
        _ = execute_query(sql_query)


def execute_query(sql_query):
    conn = None
    response = None
    try:
        # read connection parameters
        params = get_db_config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        cur.execute(sql_query)

        response = cur.fetchall()
        # print(response)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        return print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')
            if response is not None:
                return response
            else:
                return ""
