#!/usr/bin/env python

""" Is Surge Gone? """

from os import getenv
from sys import argv
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

UBER_START = '35258bbb-ea10-473d-a328-cd542f23fae8'
HOME_LAT = getenv('HOME_LAT')
HOME_LNG = getenv('HOME_LNG')
WORK_LAT = getenv('WORK_LAT')
WORK_LNG = getenv('WORK_LNG')
SERVER_TOKEN = getenv('SERVER_TOKEN')


def uber_surge_and_estimate(client, start_lat, start_lng, end_lat, end_lng):
    prices = client.get_price_estimates(start_lat, start_lng, end_lat, end_lng).json.get('prices')
    price = None
    for product in prices:
        if product['localized_display_name'] == u'uberSTART':
            price = product
    if not price:
        raise ValueError("No response from UBER")
    return price.get("estimate"), price.get("surge_multiplier")


def home_to_work(client):
    return uber_surge_and_estimate(client, HOME_LAT, HOME_LNG, WORK_LAT, WORK_LNG)


def work_to_home(client):
    return uber_surge_and_estimate(client, WORK_LAT, WORK_LNG, HOME_LAT, HOME_LNG)


def show_result(estimate, surge):
    print u"Estimate: {0}".format(estimate).encode('utf-8')
    print u"Surge: {0}".format(surge).encode('utf-8')


def main():
    """ Main scenario """
    client = UberRidesClient(Session(server_token=SERVER_TOKEN))
    func = 'work' in argv and work_to_home or home_to_work
    estimate, surge = func(client)
    show_result(estimate, surge)
    if surge > 1:
        exit(1)


if __name__ == '__main__':
    main()
