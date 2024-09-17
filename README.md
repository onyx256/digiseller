# Digiseller

[![PyPi version](https://badgen.net/pypi/v/digiseller/)](https://pypi.org/project/digiseller)
[![Загрузки](https://img.shields.io/pypi/dm/digiseller.svg)](https://pypistats.org/packages/digiseller)
[![CodeFactor](https://www.codefactor.io/repository/github/onyx256/digiseller/badge)](https://www.codefactor.io/repository/github/onyx256/digiseller)

Неофициальная библиотека - Digiseller API wrapper для Python. Простой и удобный способ взаимодействовать с АПИ сервиса.

## Установка

Установить можно используя **pip**:
```sh
pip install digiseller
```

Или напрямую с **GitHub**:
```sh
pip install git+https://github.com/onyx256/digiseller.git
```

## Использование

Пример использования библиотеки: заработок с последних 10 продаж

```python
from digiseller import Digiseller

seller_id = 123456  # https://my.digiseller.com/inside/my_info.asp?rnd=4324
api_key = 'EXAMPLE'  # https://my.digiseller.com/inside/api_keys.asp
digi = Digiseller(seller_id, api_key)

latest_sales = digi.statistics.get_latest_sales(group=False, top=10)  # Отключаем группировку по товарам, указываем top=10 чтобы получить последние 10 продаж

sales_sum = 0
for sale in latest_sales:
    sales_sum += sale.price_rub  # Имена атрибутов класса Sale соответствуют параметрам возвращаемым с API

print(f'Заработок с последних 10 продаж: {sales_sum} RUB')
```

## Доступные методы

Библиотека в разработке, доступно небольшое количество методов. **Список доступных на данный момент методов представлен ниже:**

### Статистика (api.Statistics)

- **Получение списка последних продаж**
    https://my.digiseller.com/inside/api_statistics.asp#last_sales
    ```python
    Digiseller.statistics.get_latest_sales()
    ```

- **Получение подробной статистики продаж**
    https://my.digiseller.com/inside/api_statistics.asp#last_sales

    ```python
    Digiseller.statistics.get_sales()
    ```

- **Получение статистики по продажам в качестве агента**
    https://my.digiseller.com/inside/api_statistics.asp#statistics_agent_sales

    ```python
    Digiseller.statistics.get_sales_as_agent()
    ```

### Операции (api.Operations)

- **Получение списка операций по аккаунту**
    https://my.digiseller.com/inside/api_account.asp#digiseller
    ```python
    Digiseller.operations.get_all()
    ```

- **Получение списка операций проведенных через внешних агрегаторов**
    https://my.digiseller.com/inside/api_account.asp#external

    ```python
    Digiseller.operations.external_aggregators()
    ```

- **Получение баланса личного счета**
    https://my.digiseller.com/inside/api_account.asp#view_balance

    ```python
    Digiseller.operations.get_balance()
    ```

### Товары (api.Products)

- **Получение списка категорий и их подкатегорий**
    https://my.digiseller.com/inside/api_catgoods.asp#categories
    ```python
    Digiseller.products.get_categories()
    ```

- **Получение списка товаров из категории**
    https://my.digiseller.com/inside/api_catgoods.asp#products
    ```python
    Digiseller.products.get_all_by_category()
    ```