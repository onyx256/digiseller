import hashlib
import time


def get_and_set_token(instance, token_lifespan: int = 60*120) -> (str, int):
    """
    Получение и установка токена авторизации для API
    https://my.digiseller.com/inside/api_general.asp#token

    :param instance: Экземпляр класса `Digiseller`
    :param token_lifespan: Время жизни токена в секундах, по умолчанию как в документации (120 мин)
    :return: Токен авторизации
    """
    current_time = int(time.time())
    sign = hashlib.sha256((instance.api_key + str(current_time)).encode()).hexdigest()
    data = {
        'seller_id': instance.seller_id,
        'timestamp': current_time,
        'sign': sign
    }
    resp = instance.session.post(instance.BASE_URL + 'apilogin', json=data)
    if resp.status_code == 200:
        resp_data = resp.json()
        token = resp_data.get('token')
        return token, current_time + token_lifespan
    else:
        raise ValueError(f'Не удалось получить токен:\n{resp.text}')
