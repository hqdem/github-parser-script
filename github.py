import http

import requests
from urllib.parse import urljoin


class GithubAPI:
    def __init__(self, token, base_url):
        self.base_url = base_url
        self.token = token

    def _make_request(self, path, method, query=None, data=None):
        full_url = urljoin(self.base_url, path)
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        res = requests.request(method, full_url, headers=headers, params=query, json=data)
        if res.status_code == http.HTTPStatus.FORBIDDEN:
            print(res.headers)
            print(res.text)

        try:
            res.raise_for_status()
        except requests.HTTPError as ex:
            if ex.response.status_code == http.HTTPStatus.NOT_FOUND:
                return None
            raise

        return res.json()

    def get_user_info(self, username):
        path = f'users/{username}'
        res = self._make_request(path, 'GET')
        return res

    def get_repo_contribs(self, username, repo_name):
        path = f'repos/{username}/{repo_name}/contributors'
        page = 1
        res = self._make_request(path, 'GET', query={"page": page})
        while len(res) != 0:
            for user in res:
                yield user
            page += 1
            res = self._make_request(path, 'GET', query={"page": page})
