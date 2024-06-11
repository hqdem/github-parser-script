import json

from config import Config
from github import GithubAPI


def main():
    config = Config.from_yaml('config.yaml')
    gh = GithubAPI(config.github_cfg.token, config.github_cfg.base_url)


    user_data = []
    with open('zksync.txt', 'r') as f:
        for i, repo in enumerate(f):
            print(f'processing {i} repo')
            parts = repo.strip().split('/')
            username = parts[3]
            repo_name = parts[4]

            for user in gh.get_repo_contribs(username, repo_name):
                user_data.append(user)

    with open('github-zk.json', 'w') as f:
        json.dump(user_data, f, indent=4)


if __name__ == '__main__':
    main()
