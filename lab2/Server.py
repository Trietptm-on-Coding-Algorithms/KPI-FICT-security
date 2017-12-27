import requests
from urllib.parse import urljoin


class Server:
    def __init__(self, host):
        self.__host = host

    def get(self, url, params):
        response = requests.get(urljoin(self.__host, url), params)
        return response.json()

    def post(self, url, data):
        response = requests.post(urljoin(self.__host, url), data)
        return response.json()
