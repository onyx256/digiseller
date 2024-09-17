import time

import requests
from .validators import validate_param

from . import api


class Digiseller:
    """
    Основной класс для взаимодействия с API Digiseller
    """

    BASE_URL = 'https://api.digiseller.ru/api/'

    def __init__(self, seller_id: str | int, api_key: str) -> None:
        """
        Инициализация основного класса для взаимодействия с API Digiseller

        :param seller_id: Идентификатор продавца (https://my.digiseller.com/inside/my_info.asp)
        :param api_key: API ключ для аутентификации (https://my.digiseller.com/inside/api_keys.asp)
        """

        validate_param(seller_id, (str, int), 'seller_id')
        validate_param(api_key, str, 'api_key')

        self.session: requests.Session = requests.Session()
        self.session.headers = {'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json'}

        self.seller_id: int = int(seller_id)
        self.api_key: str = api_key

        self.token: str | None = None
        self.token_expiration: int = 0

        self.operations: api.Operations = api.Operations(self)
        self.statistics: api.Statistics = api.Statistics(self)
        self.products: api.Products = api.Products(self)

    def __get_and_set_token(self) -> str:
        """
        Получает и устанавливает токен и время жизни токена
        """
        token, token_expiration = api.general.get_and_set_token(self)
        self.token = token
        self.token_expiration = token_expiration
        return token

    def __refresh_token_if_needed(self) -> None:
        """
        Обновляет токен если его время действия истекло или токен ещё не был установлен
        """
        current_time = int(time.time())
        if self.token is None or current_time >= self.token_expiration - 30:  # На всякий -30 сек от времени жизни токена
            self.__get_and_set_token()

    def make_request(self, method: str, endpoint: str, **options) -> requests.Response:
        self.__refresh_token_if_needed()

        url = self.BASE_URL + endpoint

        params = {}
        json_data = {}

        options = {k: v for k, v in options.items() if v is not None}  # Убираем все параметры None
        if method.upper() in ['GET']:
            options['token'] = self.token
            params = options
        elif method.upper() in ['POST']:
            params = {'token': self.token}
            json_data = dict(options)

        resp = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
        )
        resp.raise_for_status()

        return resp
