#!/usr/bin/env python

""" Is Surge Gone? """

from os import getenv
from requests import post
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

INFLUXDB_URL = getenv('INFLUXDB_URL', 'http://127.0.0.1:8086/write?db=uber')
HOME_LAT = getenv('HOME_LAT')
HOME_LNG = getenv('HOME_LNG')
WORK_LAT = getenv('WORK_LAT')
WORK_LNG = getenv('WORK_LNG')
VOST_LAT = getenv('VOST_LAT')
VOST_LNG = getenv('VOST_LNG')
SERVER_TOKEN = getenv('SERVER_TOKEN')
HOME_POINT = (HOME_LAT, HOME_LNG)
WORK_POINT = (WORK_LAT, WORK_LNG)
VOST_POINT = (VOST_LAT, VOST_LNG)


def uber_start_price_estimate(client, start_point, end_point):
    prices = uber_price_estimate(client, start_point, end_point)
    price = None
    for product in prices:
        if product['localized_display_name'] == u'uberSTART':
            price = product
    if not price:
        raise ValueError("No response from UBER")
    return price


def uber_price_estimate(client, start_point, end_point):
    return client.get_price_estimates(
        start_point[0], start_point[1],
        end_point[0], end_point[1]
    ).json.get('prices')


def send2influxdb(price, path):
    for key in (u'low_estimate', u'high_estimate', u'surge_multiplier'):
        data = "{0},path={1} value={2}".format(key, path, price.get(key))
        print INFLUXDB_URL, '-d', data
        post(INFLUXDB_URL, data)


def main():
    """ Main scenario """
    client = UberRidesClient(Session(server_token=SERVER_TOKEN))

    price = uber_start_price_estimate(client, HOME_POINT, WORK_POINT)
    send2influxdb(price, 'home2work')
    price = uber_start_price_estimate(client, WORK_POINT, HOME_POINT)
    send2influxdb(price, 'work2home')

    price = uber_start_price_estimate(client, WORK_POINT, VOST_POINT)
    send2influxdb(price, 'work2vost')
    price = uber_start_price_estimate(client, VOST_POINT, WORK_POINT)
    send2influxdb(price, 'vost2work')

    price = uber_start_price_estimate(client, HOME_POINT, VOST_POINT)
    send2influxdb(price, 'home2vost')
    price = uber_start_price_estimate(client, VOST_POINT, HOME_POINT)
    send2influxdb(price, 'vost2home')


if __name__ == '__main__':
    main()

