import json
import requests
from config import keys


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException('Неверное количество параметров')
        quote, base, amount = values
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}.')
        try:
            quote_formatted = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось разспознать валюту {quote}')
        try:
            base_formatted = keys[base]
        except KeyError:
            raise APIException(f'Не удалось разспознать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не получилось обработать количество {amount}')

        r = requests.get(
            f'http://api.exchangeratesapi.io/v1/latest?access_key=02c97f4b9cf77faefa3f22d77d665f8d&base={quote_formatted}&symbols={base_formatted}')
        result = float(json.loads(r.content)['rates'][base_formatted])*amount
        # total_base = round(float(amount) * float(json.loads(r.content)['rates'][keys[base]]), 2)

        return round(result, 3)
