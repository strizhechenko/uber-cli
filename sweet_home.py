#!/usr/bin/env python

import yaml
from os import getenv
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from influxdb_agent import uber_start_price_estimate

SERVER_TOKEN = getenv('SERVER_TOKEN')
ADDRESS_FILE = 'addresses.yaml'


def load_addresses():
    with open(ADDRESS_FILE, 'r') as f:
        config = yaml.load(f)
        return config


def pretty_print(results):
    print(u' UBER '.center(26, '*'))

    for rec in results:
        print(u'Addr:       {}'.format(rec.get('name')))
        print(u'Surge:      x{}'.format(rec.get('multiplier')))
        print(u'Price:      {}'.format(rec.get('price')))
        print(u'Duration    {} min'.format(rec.get('duration_sec') // 60))
        print(u'**************************')


def main():
    config = load_addresses()
    client = UberRidesClient(Session(server_token=SERVER_TOKEN))

    homes = config.get('homes')
    office = config.get('office')
    office_point = (office.get('lat'), office.get('lon'))

    results = list()
    for addr in homes:
        home_point = (addr.get('lat'), addr.get('lon'))
        estimate = uber_start_price_estimate(client, office_point, home_point)
        results.append({
            'name': addr.get('name'),
            'multiplier': estimate.get('surge_multiplier'),
            'price': estimate.get('estimate'),
            'duration_sec': estimate.get('duration'),
            })

    pretty_print(results)

if __name__ == '__main__':
    main()
