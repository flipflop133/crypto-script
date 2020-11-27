import os
import json
import requests
import time
from colorama import Fore
error_time = 0


def get_price():
    try:
        # retrieve data from json file
        with open(
                "{}/crypto_settings.json".format(
                    os.path.dirname(os.path.realpath(__file__))),
                "r") as read_file:
            data = json.load(read_file)
        url = data['url']
        currency = data['currency']
        crypto_list = data['crypto-list']
        polybar = False
        if 'polybar' in data:
            polybar = data['polybar']

        # retrieve crypto ids from json data
        ids = ""
        for crypto in range(len(crypto_list)):
            # last id
            if crypto == len(crypto_list):
                ids += "{}".format(crypto_list[crypto]['id'])
            # other ids
            else:
                ids += "{}%2C".format(crypto_list[crypto]['id'])

        # retrieve crypto data from coingecko
        request = "{}vs_currency={}&ids={}&order=market_cap_desc&per_page=100&page=1&sparkline=false".format(
            url, currency, ids)
        response = requests.get(request)
        crypto_data = json.loads(response.content)

        # display crypto properties
        for crypto in range(len(crypto_data)):
            spaces = ''
            if crypto != len(crypto_data) - 1:
                spaces = ' ' * 4
            properties = ""
            for property in crypto_list[crypto]:
                if property in crypto_data[crypto] and property != "id":
                    # current price
                    if property == "current_price":
                        if "price_precision" in crypto_list[crypto]:
                            properties += " {:.{}f} {}".format(
                                crypto_data[crypto][property],
                                crypto_list[crypto]["price_precision"],
                                currency.upper())
                        else:
                            properties += " {} {}".format(
                                crypto_data[crypto][property],
                                currency.upper())
                        # balance
                        if "balance" in crypto_list[crypto]:
                            balance = crypto_list[crypto][
                                "balance"] * crypto_data[crypto][
                                    "current_price"]
                            if "balance_precision" in crypto_list[crypto]:
                                properties += " {:.{}f} {}".format(
                                    balance,
                                    crypto_list[crypto]["balance_precision"],
                                    currency.upper())
                            else:
                                properties += " {} {}".format(
                                    balance, currency.upper())
                    elif property == "price_change_24h":
                        if "price_change_24h_precision" in crypto_list[crypto]:
                            properties += " {:.{}f}%".format(
                                crypto_data[crypto][property],
                                crypto_list[crypto]
                                ["price_change_24h_precision"])
                        else:
                            properties += " {}%".format(
                                crypto_data[crypto][property])
                    elif property == "price_change_percentage_24h":
                        # determine up or down icon
                        if polybar:
                            green = "%{F#00AA00}"
                            red = "%{F#ff0000}"
                            black = "%{F#000000}"
                        else:
                            green = Fore.GREEN
                            red = Fore.RED
                            black = Fore.RESET
                        if crypto_data[crypto][property] > 0:
                            icon = "{}".format(green)
                        else:
                            icon = "{}".format(red)
                        if "price_change_percentage_24h_precision" in crypto_list[
                                crypto]:
                            properties += " {} {:.{}f}%{}".format(
                                icon, crypto_data[crypto][property],
                                crypto_list[crypto]
                                ["price_change_percentage_24h_precision"],
                                black)
                        else:
                            properties += " {}%{}".format(
                                crypto_data[crypto][property], black)

                    # other properties
                    else:
                        properties += " {}".format(
                            crypto_data[crypto][property])
            properties += spaces
            print(properties, end="")

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
        get_price()


get_price()
