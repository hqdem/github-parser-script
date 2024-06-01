import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

import db


class User:
    def __init__(
            self,
            username,
            amount,
            url='',
            company='',
            blog='',
            location='',
            email='',
            bio='',
            twitter_username='',
            is_processed=0,
    ):
        self.username = username
        self.amount = amount
        self.url = url
        self.company = company or ''
        self.blog = blog or ''
        self.location = location or ''
        self.email = email or ''
        self.bio = bio or ''
        self.twitter_username = twitter_username or ''
        self.is_processed = is_processed

    @classmethod
    def from_row(cls, row):
        return cls(
            username=row[0],
            amount=row[1],
            url=row[2],
            company=row[3],
            blog=row[4],
            location=row[5],
            email=row[6],
            bio=row[7],
            twitter_username=row[8],
            is_processed=row[9],
        )


class DBRepo:
    def __init__(self, connection_object):
        self.conn = connection_object.connection

    def get_all_unprocessed_users(self):
        sql = sa.text("""
        SELECT *
        FROM T_USER_BIO
        WHERE is_processed=0
        ORDER BY amount desc
        """)

        with self.conn.begin():
            rows = self.conn.execute(sql).fetchall()
        res_users = []
        for row in rows:
            res_users.append(User.from_row(row))

        return res_users

    def insert_user(self, user):
        try:
            with self.conn.begin():
                sql = sa.text(f"""
                INSERT INTO T_USER_BIO
                (username, amount, url, company, blog, location, email, bio, twitter_username)
                VALUES
                (
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.username)},
                    {user.amount},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.url)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.company)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.blog)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.location)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.email)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.bio)},
                    {sa.String(0, '').literal_processor(self.conn.dialect)(value=user.twitter_username)}
                )
                """)

                self.conn.execute(sql)
        except IntegrityError as ex:
            print(f"can not insert user {user.username}. error info {ex}")

    def update_user_info(self, user):
        sql = sa.text(f"""
        UPDATE T_USER_BIO
        SET 
            url={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.url)},
            company={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.company)},
            blog={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.blog)},
            location={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.location)},
            email={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.email)},
            bio={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.bio)},
            twitter_username={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.twitter_username)},
            is_processed={user.is_processed}
            
        WHERE username={sa.String(0, '').literal_processor(self.conn.dialect)(value=user.username)}
        """)

        try:
            with self.conn.begin():
                self.conn.execute(sql)
        except Exception as ex:
            print(f"can not update user {user.username}. error info {ex}")


if __name__ == '__main__':
    u = User(
        username='test',
        amount=100000,
        url="jonh' snow",
        company="test' company' of' test"
    )

    db_conn = db.SqliteDbConn()
    db = DBRepo(db_conn)
    db.update_user_info(u)
