#!/usr/bin/env python

""" Is Surge Gone? """

from os import getenv
from sys import argv
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from influxdb_agent import uber_start_price_estimate, get_point

PLACES = getenv('PLACES').split()
SERVER_TOKEN = getenv('SERVER_TOKEN')


def show_result(estimate, surge):
    print u"Estimate: {0}".format(estimate).encode('utf-8')
    print u"Surge: {0}".format(surge).encode('utf-8')


def main():
    """ Main scenario """
    client = UberRidesClient(Session(server_token=SERVER_TOKEN))
    src, dst = argv[1], argv[2]
    points = {k: get_point(k) for k in PLACES}
    estimate, surge = uber_start_price_estimate(client, points.get(src), points.get(dst))
    show_result(estimate, surge)
    if surge > 1:
        exit(1)


if __name__ == '__main__':
    main()
