import requests
import json
from pass_key import exchanges

class ConvertionException(Exception):
    pass

class Conversion:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно конвертировать одинаковые валюты (из {quote} в {base})")

        try:
            quote_ticker = exchanges[quote]
        except KeyError:
            raise ConvertionException(f"Либо вы ввели валюту, с которой я не работаю\nЛибо допустили ошибку при вводе" \
                                      f" валюты: {quote}\nПроверить доступные валюты можно по команде /values")

        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise ConvertionException(f"Либо вы ввели валюту, с которой я не работаю\nЛибо допустили ошибку при вводе" \
                                      f" валюты: {base}\nПроверить доступные валюты можно по команде /values")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"{amount} - неправильная форма количества, введите число")


        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        answer = json.loads(r.content)[exchanges[base]] * amount
        return answer