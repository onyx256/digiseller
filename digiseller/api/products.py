from typing import Optional, List

from digiseller.api import ApiCategoryBase


class Category:
    """
    Представляет информацию о категории
    https://my.digiseller.com/inside/api_catgoods.asp#categories
    """

    def __init__(self, _id: int, name: str, products_count: int, subcategories: Optional[List['Category']]) -> None:
        self.id: int = _id
        self.name: str = name
        self.products_count: int = products_count
        self.subcategories: List[Category] = subcategories

    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        subcategories_raw = data.get('sub')
        if subcategories_raw:
            subcategories = [Category.from_dict(subcategory_raw) for subcategory_raw in subcategories_raw]
        else:
            subcategories = None

        return cls(
            _id=data['id'],
            name=data['name'],
            products_count=data['products_count'],
            subcategories=subcategories
        )


class Product:
    """
    Представляет информацию о товаре
    https://my.digiseller.com/inside/api_catgoods.asp#products
    """

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {self.__dict__}>'

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        return cls(**data)


class Products(ApiCategoryBase):
    """
    Класс для взаимодействия с товарами и категориями
    """

    def __init__(self, digiseller) -> None:
        super().__init__(digiseller)

    def get_categories(self,
                       seller_id: Optional[int] = None,
                       category_id: int = 0,
                       lang: str = 'ru-RU'
                       ) -> List[Category]:
        """
        Получение списка категорий и их подкатегорий
        https://my.digiseller.com/inside/api_catgoods.asp#categories

        :param seller_id: ID продавца
        :param category_id: ID категории; по умолчанию - 0 (все категории)
        :param lang: Язык отображения информации (ru-RU/en-US)
        """
        if not seller_id:
            seller_id = self.digiseller.seller_id

        resp = self.digiseller.make_request(
            'get', 'categories',
            seller_id=seller_id,
            category_id=category_id,
            lang=lang
        )

        data = resp.json()
        categories_raw = data['category']
        categories = [Category.from_dict(category_raw) for category_raw in categories_raw]

        return categories

    def get_all_by_category(self,
                            seller_id: Optional[int] = None,
                            category_id: int = 0,
                            page: int = 1,
                            rows: int = 20,
                            order: Optional[str] = None,
                            currency: str = 'RUR',
                            lang: str = 'ru-RU') -> List[Product]:
        """
        Получение списка товаров из категории
        https://my.digiseller.com/inside/api_catgoods.asp#products

        :param seller_id: ID продавца
        :param category_id: ID категории; по умолчанию - 0 (все категории)
        :param page: Номер страницы
        :param rows: Количество товаров на одной странице
        :param order: Способ сортировки товаров
        :param currency: Тип валюты для отображения товара
        :param lang: Язык отображения информации (ru-RU/en-US)
        """
        if not seller_id:
            seller_id = self.digiseller.seller_id

        resp = self.digiseller.make_request(
            'get', 'shop/products',
            seller_id=seller_id,
            category_id=category_id,
            page=page,
            rows=rows,
            order=order,
            currency=currency,
            lang=lang
        )
        data = resp.json()
        products_raw = data['product']
        products = [Product.from_dict(product_raw) for product_raw in products_raw]

        return products
