import requests
import json

class APIException(Exception):
    pass


class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Некорректное количество: {amount}")

        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException(f"Ошибка запроса к API: {response.status_code}")

        data = json.loads(response.text)
        if quote not in data['rates']:
            raise APIException(f"Валюта {quote} не найдена.")
        if base not in data['rates']:
            raise APIException(f"Валюта {base} не найдена.")

        rate = data['rates'][quote]
        return rate * amount