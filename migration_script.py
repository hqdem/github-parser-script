import json
from db_repo import User, DBRepo
from config import Config
from db import SqliteDbConn

FILE_COUNT = 3
FILE_FORMAT = 'github-{}.json'


def main():
    cfg = Config.from_yaml('config.yaml')
    db_conn = SqliteDbConn(
        filename=cfg.db_cfg.filename,
    )
    db = DBRepo(db_conn)

    for i in range(FILE_COUNT):
        with open(FILE_FORMAT.format(i), 'r') as f:
            data = json.load(f)

        users = data['eligibles']
        users_count = len(users)
        for j, user in enumerate(users):
            print(f"processed {j + 1} row of {users_count} rows")
            users_object = User(username=user['identity'], amount=user['amount'])
            db.insert_user(users_object)


if __name__ == '__main__':
    main()
