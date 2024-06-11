import json
import time

import sqlalchemy as sa
import requests

import db

url = 'https://api.zknation.io/eligibility'


def create_zk_table(conn):
    sql = sa.sql.text("""
        CREATE TABLE IF NOT EXISTS T_ZKSYNC_ELIGIBLE  (
            username TEXT PRIMARY KEY,
            id INTEGER NOT NULL,
            is_eligible BOOL NOT NULL,
            is_processed BOOL NOT NULL DEFAULT 0
        );
    """)
    conn.execute(sql)
    conn.commit()


def insert_user(conn, username, user_id):
    sql = sa.sql.text(f"""
        INSERT INTO T_ZKSYNC_ELIGIBLE
        (username, id, is_eligible)
        VALUES
        ('{username}', {user_id}, false)
    """)
    conn.execute(sql)
    conn.commit()


def process_user(conn, username, is_eligible):
    sql = sa.sql.text(f"""
        UPDATE T_ZKSYNC_ELIGIBLE
        SET is_eligible={is_eligible}, is_processed=true
        WHERE username='{username}'
    """)
    conn.execute(sql)
    conn.commit()


def get_all_unprocessed_users(conn):
    sql = sa.sql.text("""
    SELECT *
    FROM T_ZKSYNC_ELIGIBLE
    WHERE is_processed=false
    """)

    return conn.execute(sql).fetchall()


def main():
    db_con = db.SqliteDbConn('sqlite3.db').connection

    # create_zk_table(db_con)
    #
    # for i, user in enumerate(data):
    #     print(f'processing {i} user of {count}')
    #     user_id = user['id']
    #     username = user['login']
    #
    #     try:
    #         insert_user(db_con, username, user_id)
    #     except Exception as ex:
    #         print(ex)

    data = get_all_unprocessed_users(db_con)
    count = len(data)
    print(len(data))

    for i, user in enumerate(data):
        print(f'processing {i} user of {count}')

        username = user[0]
        user_id = user[1]
        params = {
            'id': user_id
        }
        headers = {
            'X-Api-Key': '46001d8f026d4a5bb85b33530120cd38'
        }
        req = requests.get(url, params=params, headers=headers)
        res = req.json()

        is_eligible = len(res['allocations']) != 0
        process_user(db_con, username, is_eligible)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
