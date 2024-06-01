import yaml


class SqliteDBConfig:
    def __init__(
            self,
            filename,
    ):
        self.filename = filename


class GithubConfig:
    def __init__(
            self,
            token,
            base_url,
    ):
        self.token = token
        self.base_url = base_url


class Config:
    def __init__(
            self,
            github_cfg,
            db_cfg,
    ):
        self.github_cfg = github_cfg
        self.db_cfg = db_cfg

    @classmethod
    def from_yaml(cls, cfg_path):
        with open(cfg_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls._from_dict(data)

    @classmethod
    def _from_dict(cls, dict_data):
        return cls(
            github_cfg=GithubConfig(token=dict_data['github']['token'], base_url=dict_data['github']['base_url']),
            db_cfg=SqliteDBConfig(filename=dict_data['db']['filename'])
        )
