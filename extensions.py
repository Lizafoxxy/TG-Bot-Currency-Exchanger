import requests
import json
from config import keys

# класс исключений, для обработки ошибок  пользователя при направлении запроса
class APIException(Exception):
    pass

class CurrencyConverter:  # класс со статическим методом для обработки конвертации
    @staticmethod
    def get_price(base: str, quote: str, amount: str):  # чтобы метод работал, ему надо передать сообщение
        # обрабатываем еще одно исключение - если пользователь ввел две одинаковые валюты:
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты - {base}.')

        # вводим  переменные quote_ticker и base_ticker, чтобы
        # обрабатывать ошибки пользователя при вводе наименований валюты
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {quote}')
        # обрабатываем ошибку, если amount будет введен в виде строкового значения:
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')

        total_base = json.loads(r.content)[keys[quote]]

        return total_base