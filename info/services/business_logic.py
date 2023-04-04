import copy
import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler

__path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d&locale=en'
__response = requests.get(__path).json()
__data = json.dumps(__response)
__data = json.loads(__data)


def request_data_from_coin_gecko_api():
    global __data
    global __path
    response = requests.get(__path).json()
    __data = json.dumps(response)
    __data = json.loads(__data)


def job():
    request_data_from_coin_gecko_api()


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=10)
scheduler.start()


def get_crypto_data_from_coin_gecko(user_is_authorized, sorting=None):
    return get_250_coins(sorting) if user_is_authorized else get_10_coins()


def get_10_coins():
    global __data
    data = copy.deepcopy(__data)
    list_10_coins = []
    for index in range(10):
        list_10_coins.append(data[index])
    for info in list_10_coins:
        info['symbol'] = info['symbol'].upper()
        info['current_price'] = round(info['current_price'], 9)
    return list_10_coins


def get_250_coins(sorting):
    global __data
    data = copy.deepcopy(__data)
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
    sorted_list = sorted(data, key=lambda d: d[sorting], reverse=True)
    for info in sorted_list:
        volume = info['total_volume']
        info['total_volume'] = f'{volume:,}'.replace(',', ' ')
    return sorted_list
