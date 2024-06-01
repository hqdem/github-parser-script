import enum
import re

from config import Config
from db import SqliteDbConn
from db_repo import DBRepo, User
from github import GithubAPI


EMAIL_PATTERN = r"\S+@\S+\.\S+"


class CfgTypeLoader(enum.Enum):
    YAML = 'yaml'


class BioParser:
    def __init__(self, cfg_path, cfg_type=CfgTypeLoader.YAML.value):
        if cfg_type == CfgTypeLoader.YAML.value:
            self.config = Config.from_yaml(cfg_path)
        else:
            raise AttributeError('unknown config file type')

        conn = SqliteDbConn(filename=self.config.db_cfg.filename)
        self.db = DBRepo(conn)
        self.github_api = GithubAPI(
            base_url=self.config.github_cfg.base_url,
            token=self.config.github_cfg.token
        )

    def parse(self):
        users = self.db.get_all_unprocessed_users()
        users_count = len(users)
        for i, user in enumerate(users):
            print(f"processing {i + 1} of {users_count} users")
            # time.sleep(0.1)
            data = self.github_api.get_user_info(user.username)
            if data is None:
                continue

            email = data['email']
            if email is None or email == '':
                bio = data['bio'] or ''
                emails = re.findall(EMAIL_PATTERN, bio)
                if len(emails) > 0:
                    email = emails[1]

            updated_user = User(
                username=data['login'],
                amount=None,  # тут не надо
                url=data['html_url'],
                company=data['company'],
                blog=data['blog'],
                location=data['location'],
                email=email,
                bio=data['bio'],
                twitter_username=data['twitter_username'],
                is_processed=1,
            )
            self.db.update_user_info(updated_user)


if __name__ == '__main__':
    b = BioParser('config.yaml')
    b.parse()
