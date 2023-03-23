import requests
import json


def get_crypto_data_from_coin_gecko(user_is_authorized):
    return get_250_coins() if user_is_authorized else get_10_coins()


def get_10_coins():
    path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false'
    response = requests.get(path).json()
    data = json.dumps(response)
    data = json.loads(data)
    info_list = []
    for inf in data:
        info = {"image": inf['image'], "name": inf['name'], "symbol": str(inf['symbol']).upper(),
                "current_price": round(inf['current_price'], 9)}
        info_list.append(info)
    return info_list


def get_250_coins():
    path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d'
    response = requests.get(path).json()
    data = json.dumps(response)
    data = json.loads(data)
    info_list = []
    for inf in data:
        info = {}
        changes_for_1h = inf['price_change_percentage_1h_in_currency']
        changes_for_24h = inf['price_change_percentage_24h']
        changes_for_7d = inf['price_change_percentage_7d_in_currency']
        changes_for_1h = changes_for_1h if changes_for_1h is not None else 0.0
        changes_for_24h = changes_for_24h if changes_for_24h is not None else 0.0
        changes_for_7d = changes_for_7d if changes_for_7d is not None else 0.0
        info["image"] = inf['image']
        info["name"] = inf['name']
        info["symbol"] = str(inf['symbol']).upper()
        info["current_price"] = round(inf['current_price'], 9)
        info["changes_for_1h"] = round(changes_for_1h, 1)
        info["changes_for_24h"] = round(changes_for_24h, 1)
        info["changes_for_7d"] = round(changes_for_7d, 1)
        info["total_volume"] = "{:,}".format(inf['total_volume'])
        info_list.append(info)
    return info_list
