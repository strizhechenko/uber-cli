#!/usr/bin/env python

""" Is Surge Gone? """

from os import getenv
from itertools import product
from requests import post
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

INFLUXDB_URL = getenv('INFLUXDB_URL', 'http://127.0.0.1:8086/write?db=uber')
SERVER_TOKEN = getenv('SERVER_TOKEN')


def get_point(name):
    return (getenv("{0}_LAT".format(name.upper())), getenv("{0}_LNG".format(name.upper())))


def get_places():
    places = getenv('PLACES')
    return places.split() if places else list()


def get_blacklist():
    blacklisted = getenv('BLACKLISTED_ROUTES')
    return blacklisted.split() if blacklisted else list()


def uber_start_price_estimate(client, start_point, end_point):
    prices = uber_price_estimate(client, start_point, end_point)
    price = None
    for uber_type in prices:
        if uber_type['localized_display_name'] == u'uberSTART':
            price = uber_type
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
    places = get_places()
    points = {k: get_point(k) for k in places}
    blacklist = get_blacklist()
    for route in product(places, places):
        route_name = "{0}2{1}".format(route[0], route[1])
        if route[0] == route[1] or route_name in blacklist:
            continue
        price = uber_start_price_estimate(client, points[route[0]], points[route[1]])
        send2influxdb(price, route_name)


if __name__ == '__main__':
    main()
