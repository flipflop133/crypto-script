import os
import json
import requests
import time
from colorama import Fore
error_time = 0


def main():
    try:
        # retrieve data from json file
        data = get_data()
        url = data['url']
        url_2 = data['url_2']
        currency = data['currency']
        crypto_list = data['crypto-list']
        polybar = False
        if 'polybar' in data:
            polybar = data['polybar']

        # retrieve crypto ids from json data
        ids = get_crypto_ids(crypto_list)

        # retrieve crypto data from coingecko
        request = "{}vs_currency={}&ids={}{}".format(url, currency, ids, url_2)
        response = requests.get(request)
        crypto_data = json.loads(response.content)

        # display crypto
        display_crypto(currency, crypto_list, polybar, crypto_data)

    # errors handling
    except OSError:
        print("crypto_settings.json file not found")
    except json.JSONDecodeError:
        print("error in crypto_settings.json file")
    except Exception as e:
        print(e)
        global error_time
        time.sleep(error_time)
        error_time += 10
        print(error_time)
        main()


def get_data():
    with open(
            "{}/crypto_settings.json".format(
                os.path.dirname(os.path.realpath(__file__))),
            "r") as read_file:
        return json.load(read_file)


def get_crypto_ids(crypto_list):
    ids = ""
    for crypto in range(len(crypto_list)):
        # last id
        if crypto == len(crypto_list):
            ids += "{}".format(crypto_list[crypto]['id'])
        # other ids
        else:
            ids += "{}%2C".format(crypto_list[crypto]['id'])
    return ids


def display_crypto(currency, crypto_list, polybar, crypto_data):
    # display crypto properties
    display_crypto = ""
    for crypto in range(len(crypto_data)):
        # determine spaces between different crypto
        spaces = ''
        if crypto != len(crypto_data) - 1:
            spaces = ' ' * 4

        # retrieve each crypto properties
        properties = get_properties(currency, crypto_list, polybar,
                                    crypto_data, crypto)

        # add spaces between each crypto
        properties += spaces
        display_crypto += properties
    print(display_crypto)


def get_properties(currency, crypto_list, polybar, crypto_data, crypto):
    properties = ""
    add_space = False
    for property in crypto_list[crypto]:
        if property in crypto_data[crypto] and property != "id":
            # determine space to add between each property
            if add_space:
                space = ' '
            else:
                space = ''

            # current_price
            if property == "current_price":
                properties = current_price(currency, crypto_list, crypto_data,
                                           crypto, properties, property, space)

            # price_change_24h
            elif property == "price_change_24h":
                if "price_change_24h_precision" in crypto_list[crypto]:
                    properties += "{}{:.{}f}%".format(
                        space, crypto_data[crypto][property],
                        crypto_list[crypto]["price_change_24h_precision"])
                else:
                    properties += "{}{}%".format(space,
                                                 crypto_data[crypto][property])
            # price_change_percentage_24h
            elif property == "price_change_percentage_24h":
                properties = price_change_percentage_24h(
                    crypto_list, polybar, crypto_data, crypto, properties,
                    property, space)
            # other properties
            else:
                properties += "{}{}".format(space,
                                            crypto_data[crypto][property])
            add_space = True

    return properties


def current_price(currency, crypto_list, crypto_data, crypto, properties,
                  property, space):
    # price
    if "price_precision" in crypto_list[crypto]:
        properties += "{}{:.{}f} {}".format(
            space, crypto_data[crypto][property],
            crypto_list[crypto]["price_precision"], currency.upper())
    else:
        properties += "{}{} {}".format(space, crypto_data[crypto][property],
                                       currency.upper())
    # balance
    if "balance" in crypto_list[crypto]:
        balance = crypto_list[crypto]["balance"] * crypto_data[crypto][
            "current_price"]
        if "balance_precision" in crypto_list[crypto]:
            properties += "{}{:.{}f} {}".format(
                space, balance, crypto_list[crypto]["balance_precision"],
                currency.upper())
        else:
            properties += "{}{} {}".format(space, balance, currency.upper())

    return properties


def price_change_percentage_24h(crypto_list, polybar, crypto_data, crypto,
                                properties, property, space):
    # determine up or down icon
    if polybar:
        green = "%{F#00AA00}"
        red = "%{F#ff0000}"
        black = "%{F#000000}"
    else:
        green = Fore.GREEN
        red = Fore.RED
        black = Fore.RESET

    # determine price_change_percentage_24h
    if crypto_data[crypto][property] > 0:
        icon = "{}".format(green)
    else:
        icon = "{}".format(red)
    if "price_change_percentage_24h_precision" in crypto_list[crypto]:
        properties += "{}{} {:.{}f}%{}".format(
            space, icon, crypto_data[crypto][property],
            crypto_list[crypto]["price_change_percentage_24h_precision"],
            black)
    else:
        properties += "{}{}%{}".format(space, crypto_data[crypto][property],
                                       black)

    return properties


main()
