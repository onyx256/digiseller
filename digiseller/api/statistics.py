from datetime import datetime
from typing import List, Optional

from digiseller.api import ApiCategoryBase


class Sale:
    """
    Представляет информацию о продаже
    https://my.digiseller.com/inside/api_statistics.asp
    """

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.__dict__}>'

    @classmethod
    def from_dict(cls, data: dict) -> 'Sale':
        return cls(**data)


class Statistics(ApiCategoryBase):
    """
    Класс для взаимодействия со статистикой продаж
    """

    def __init__(self, digiseller) -> None:
        super().__init__(digiseller)

    def get_latest_sales(self, group: bool = True, top: int = 1000) -> List[Sale]:
        """
        Получение списка последних продаж.
        https://my.digiseller.com/inside/api_statistics.asp#last_sales

        :param group: Флаг для группировки результатов по товарам. Если True, то результаты будут отсортированы по товарам. Если False, то результаты будут отсортированы по дате продажи.
        :param top: Количество последних продаж для получения.

        :return: Список объектов `Sale`, представляющих информацию о продаже
        """
        resp = self.digiseller.make_request(
            'get', 'seller-last-sales',
            seller_id=self.digiseller.seller_id,
            group=group,
            top=top
        )

        data = resp.json()
        last_sales_raw = data['sales']
        sales = [Sale.from_dict(last_sale_raw['product']) for last_sale_raw in last_sales_raw]

        return sales

    def get_sales(self,
                  product_ids: Optional[List[int]] = None,
                  date_start: datetime = datetime(2000, 1, 1, 0, 0, 0),
                  date_finish: datetime = datetime.now(),
                  returned: int = 0,
                  page: int = 1,
                  rows: int = 10) -> List[Sale]:
        """
        Получение подробной статистики по продажам.
        https://my.digiseller.com/inside/api_statistics.asp#statisticsells

        :param product_ids: Список ID товаров, по которым нужно получить статистику. Если не указано, то будет возвращена статистика по всем товарам.
        :param date_start: Дата начала. По умолчанию - 2000 год (чтобы получить все продажи)
        :param date_finish: Дата конца. По умолчанию - текущая дата и время
        :param returned: 0 - включить возвраты; 1 - без возвратов; 2 - только возвраты
        :param page: Номер страницы
        :param rows: Количество продаж на одной странице. До 100 продаж.

        :return: Список объектов `Sale`, представляющих информацию о продаже
        """
        resp = self.digiseller.make_request(
            'post', 'seller-sells/v2',
            product_ids=product_ids,
            date_start=date_start.strftime('%Y-%m-%d %H:%M:%S'),
            date_finish=date_finish.strftime('%Y-%m-%d %H:%M:%S'),
            returned=returned,
            page=page,
            rows=rows
        )
        data = resp.json()
        sales_raw = data['rows']
        sales = [Sale.from_dict(sale_raw) for sale_raw in sales_raw]

        return sales

    def get_sales_as_agent(self,
                           partner_id: Optional[int] = None,
                           product_ids: Optional[List[int]] = None,
                           date_start: datetime = datetime(2000, 1, 1, 0, 0, 0),
                           date_finish: datetime = datetime.now(),
                           returned: int = 0,
                           page: int = 0,
                           rows: int = 10
                           ):
        """
            Получение статистики по продажам в качестве агента
            https://my.digiseller.com/inside/api_statistics.asp#statistics_agent_sales

            :param partner_id: ID партнера
            :param product_ids: Список ID товаров, по которым нужно получить статистику. Если не указано, то будет возвращена статистика по всем товарам.
            :param date_start: Дата начала. По умолчанию - 2000 год (чтобы получить все продажи)
            :param date_finish: Дата конца. По умолчанию - текущая дата и время
            :param returned: 0 - включить возвраты; 1 - без возвратов; 2 - только возвраты
            :param page: Номер страницы
            :param rows: Количество продаж на одной странице. До 1000 продаж.

            :return: Список объектов `Sale`, представляющих информацию о продаже
        """
        resp = self.digiseller.make_request(
            'post', 'agent-sales/v2',
            id_partner=partner_id,
            product_ids=product_ids,
            date_start=date_start.strftime('%Y-%m-%d %H:%M:%S'),
            date_finish=date_finish.strftime('%Y-%m-%d %H:%M:%S'),
            returned=returned,
            page=page,
            rows=rows
        )
        data = resp.json()
        sales_raw = data['rows']
        sales = [Sale.from_dict(sale_raw) for sale_raw in sales_raw]

        return sales
