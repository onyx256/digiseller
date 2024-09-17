# Digiseller

Неофициальная библиотека - Digiseller API wrapper для Python. Простой и удобный способ взаимодействовать с АПИ сервиса.

[![Загрузки](https://img.shields.io/pypi/dm/digiseller.svg)](https://pypistats.org/packages/digiseller)
[![CodeFactor](https://www.codefactor.io/repository/github/onyx256/digiseller/badge)](https://www.codefactor.io/repository/github/onyx256/digiseller)

## Установка

Установить можно используя pip:
```sh
pip install digiseller
```

Или напрямую с GitHub:
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