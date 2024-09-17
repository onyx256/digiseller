from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List


class Currency(Enum):
    WMR = 'WMR'
    WMZ = 'WMZ'
    WME = 'WME'


class OperationType(Enum):
    AGENT_ACCURALS = 'agent_accurals'
    PRODUCT_SALES = 'product_sales'
    ADD_FUNDS = 'add_funds'
    EXCHANGE_RESPONSE = 'exchange_response'
    EXCHANGE_REQUEST = 'exchange_request'
    REFUND = 'refund'
    ADV_GOOD = 'adv_goods'
    EXTERNAL_COMMISSIONS = 'external_commissions'
    HARD_DISK_RENT = 'hard_disk_rent'
    EXTRA_PARTNER_SPACE = 'extra_partner_space'
    GIFT_CERTIFICATES = 'gift_certificates'
    TRANSFER_TO_WALLET = 'transfer_to_wallet'


class CodeFilter(Enum):
    ONLY_WAITING_CHECK_CODE = 'only_waiting_check_code'
    HIDE_WAITING_CODE_CHECK = 'hide_waiting_code_check'


class AllowType(Enum):
    EXCLUDE = 'exclude'
    ONLY = 'only'


class Operation:
    """
    Представляет информацию об операции
    https://my.digiseller.com/inside/api_account.asp
    """

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.__dict__}>'

    @classmethod
    def from_dict(cls, data: dict) -> 'Operation':
        return cls(**data)


class Operations:
    """
    Класс для взаимодействия с операциями по аккаунту
    """

    def __init__(self, digiseller) -> None:
        self.digiseller = digiseller

    def get_all(self,
                page: int = 1,
                count: int = 10,
                currency: Optional[Currency | str] = None,
                operation_type: Optional[OperationType | str] = None,
                code_filter: Optional[CodeFilter | str] = None,
                allow_type: Optional[AllowType | str] = None,
                date_start: datetime = (datetime.now() - timedelta(weeks=2)).strftime('%Y-%m-%dT%H:%M'),
                date_finish: datetime = datetime.now().strftime('%Y-%m-%dT%H:%M')) -> List[Operation]:
        """
        Получение списка операций по аккаунту
        https://my.digiseller.com/inside/api_account.asp#digiseller

        :param page: Номер страницы
        :param count: Количество отображаемых операций (до 200)
        :param currency: Валюта (Currency/str)
        :param operation_type: Тип операции (OperationType/str)
        :param code_filter: Операции, ожидающие проверки уникального кода (CodeFilter/str)
        :param allow_type: Операции недоступные для вывода (AllowType/str)
        :param date_start: Дата начала. По умолчанию - 2 недели назад
        :param date_finish: Дата конца. По умолчанию - текущая дата и время

        :return: Список объектов `Operation`, представляющих информацию об операции
        """
        resp = self.digiseller.make_request(
            'get', 'sellers/account/receipts',
            page=page,
            count=count,
            currency=currency.value if isinstance(currency, Currency) else currency,
            type=operation_type.value if isinstance(operation_type, OperationType) else operation_type,
            codeFilter=code_filter.value if isinstance(code_filter, CodeFilter) else code_filter,
            allowType=allow_type.value if isinstance(allow_type, AllowType) else allow_type,
            start=date_start,
            finish=date_finish
        )
        data = resp.json()
        items = data['content']['items']
        operations = [Operation.from_dict(item) for item in items]

        return operations

    def external_aggregators(self,
                             page: int = 1,
                             count: int = 10,
                             order: str = 'Date DESC',
                             allow_type: Optional[AllowType | str] = None,
                             aggregator: Optional[str] = 'freekassa'):
        """
        Получение списка операций проведенных через внешних агрегаторов
        https://my.digiseller.com/inside/api_account.asp#external

        :param page: Номер страницы
        :param count: Количество операций на одной странице
        :param order: Сортировка
        :param allow_type: Операции недоступные для вывода (AllowType/str)
        :param aggregator: Агрегатор (платежная система). Например: 'yandex' - ЮMoney, 'enot' - Enot.io

        :return: Список объектов `Operation`, представляющих информацию об операции
        """
        resp = self.digiseller.make_request(
            'get', 'sellers/account/receipts/external',
            page=page,
            count=count,
            order=order,
            code=allow_type,
            aggregator=aggregator
        )
        data = resp.json()
        items = data['content']['items']
        operations = [Operation.from_dict(item) for item in items]

        return operations

    def get_balance(self) -> dict:
        """
        Получение баланса личного счета
        https://my.digiseller.com/inside/api_account.asp#view_balance

        :return: Словарь представляющий баланс счета
        """
        resp = self.digiseller.make_request('get', 'sellers/account/balance/info')

        data = resp.json()
        balances = data['content']

        return balances
