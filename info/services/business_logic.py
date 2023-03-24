import requests
import json


def get_crypto_data_from_coin_gecko(user_is_authorized):
    return get_250_coins() if user_is_authorized else get_10_coins()


def get_10_coins():
    path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false'
    response = requests.get(path).json()
    data = json.dumps(response)
    data = json.loads(data)
    for info in data:
        info['symbol'] = info['symbol'].upper()
        info['current_price'] = round(info['current_price'], 9)
    return data


def get_250_coins():
    path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d'
    response = requests.get(path).json()
    data = json.dumps(response)
    data = json.loads(data)
    for info in data:
        changes_for_1h = info['price_change_percentage_1h_in_currency']
        changes_for_24h = info['price_change_percentage_24h']
        changes_for_7d = info['price_change_percentage_7d_in_currency']
        changes_for_1h = changes_for_1h if changes_for_1h is not None else 0.0
        changes_for_24h = changes_for_24h if changes_for_24h is not None else 0.0
        changes_for_7d = changes_for_7d if changes_for_7d is not None else 0.0
        info["symbol"] = str(info['symbol']).upper()
        info["current_price"] = round(info['current_price'], 9)
        info["price_change_percentage_1h_in_currency"] = round(changes_for_1h, 1)
        info["price_change_percentage_24h"] = round(changes_for_24h, 1)
        info["price_change_percentage_7d_in_currency"] = round(changes_for_7d, 1)
        info["total_volume"] = "{:,}".format(info['total_volume'])
    return data
