import sqlalchemy as sa


class SqliteDbConn:
    def __init__(self, filename='sqlite.db'):
        engine = sa.create_engine(f"sqlite:///{filename}")
        self.connection = engine.connect()
        self._on_start()

    def _on_start(self):
        create_table_sql = sa.sql.text("""
        CREATE TABLE IF NOT EXISTS T_USER_BIO (
            username TEXT PRIMARY KEY,
            amount NUMBER NUT NULL,
            url TEXT NOT NULL,
            company TEXT,
            blog TEXT,
            location TEXT,
            email TEXT,
            bio TEXT,
            twitter_username TEXT,
            is_processed INTEGER NOT NULL DEFAULT 0
        );
        """)
        self.connection.execute(create_table_sql)
        self.connection.commit()
