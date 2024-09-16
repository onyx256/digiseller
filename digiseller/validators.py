def validate_param(param, expected_types, param_name) -> None:
    """
    Проверяет, что параметр соответствует ожидаемым типам и не пуст, если str

    :param param: Параметр для проверки
    :param expected_types: Ожидаемый тип или кортеж типов
    :param param_name: Имя параметра для использования в сообщениях об ошибках
    """
    if not isinstance(param, expected_types):
        raise TypeError(f'`{param_name}` должен быть {expected_types}, получен {type(param).__name__}')

    if isinstance(param, str) and not param.strip():
        raise ValueError(f'`{param_name}` не может быть пустым')
