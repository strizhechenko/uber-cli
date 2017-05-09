#!/usr/bin/env python

import os
import time
import optparse
import yaml
from pygeocoder import Geocoder
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from uber_cli import writers


class Place(object):
    def __init__(self, addr, conf):
        self.addr = unicode(addr, 'utf-8')
        self.city = conf.get('DEFAULT_CITY')

    def with_city(self):
        return u"{0}, {1}".format(self.city, self.addr)


class UberCLI(object):
    def __init__(self):
        self.conf = self.read_config()
        self.options, self.args = self.read_options()
        self.writer = self.choose_writer()(self.options)
        assert len(self.args) == 2, "Usage: uber-cli <src> <dst>"
        self.places = {
            "src": Place(self.args[0], self.conf),
            "dst": Place(self.args[1], self.conf),
        }

    def choose_writer(self):
        if self.options.dict_writer:
            return writers.DictWriter
        if self.options.influxdb_writer:
            return writers.InfluxWriter
        return writers.PlainWriter

    @staticmethod
    def alert(message):
        print message
        os.system("say {0}".format(message))

    @staticmethod
    def read_options():
        parser = optparse.OptionParser()
        parser.add_option('-i', dest='interval', type="int", metavar='SECONDS', default=30,
                          help='delay between queries')
        parser.add_option('-w', '--watch', dest='watch', action='store_true', default=False, help='run query loop')
        parser.add_option('-o', '--one-line', dest='plain_writer', action='store_true', default=False, help='writer format')
        parser.add_option('-d', '--dict', dest='dict_writer', action='store_true', default=False, help='writer format')
        parser.add_option('--influxdb-format', dest='influxdb_writer', action='store_true', default=False, help='writer format')
        parser.add_option('--influxdb-url', dest='influxdb', metavar='URL',
                          help='Example: http://127.0.0.1:8086/write?db=my_db')
        parser.add_option('-f', '--fair-price', dest='fair_price', type="int",
                          help='defines fair price that ok to order taxi')
        return parser.parse_args()

    @staticmethod
    def read_config():
        conf_file = os.path.join(os.getenv('HOME'), '.uberrc')
        if not os.path.exists(conf_file):
            return {}
        with open(conf_file) as conf_fd:
            return yaml.load(conf_fd)

    def geocode(self):
        geocoder = Geocoder()
        src = geocoder.geocode(self.places['src'].with_city()).coordinates
        dst = geocoder.geocode(self.places['dst'].with_city()).coordinates
        return src, dst

    def price(self, src, dst):
        client = UberRidesClient(Session(server_token=self.conf.get('SERVER_TOKEN')))
        return client.get_price_estimates(src[0], src[1], dst[0], dst[1]).json.get('prices')

    def oneshot(self, src, dst):
        price = self.price(src, dst)
        self.writer.write(price, self.places)
        if self.options.fair_price and price[0].get(u'low_estimate') < self.options.fair_price:
            self.alert(self.conf.get('PHRASE'))
            exit(0)

    def watch(self, src, dst):
        try:
            self.writer.header()
            while True:
                self.oneshot(src, dst)
                time.sleep(self.options.interval)
        except KeyboardInterrupt:
            exit(0)

    def main(self):
        src, dst = self.geocode()
        if self.options.watch:
            self.watch(src, dst)
        else:
            self.oneshot(src, dst)

if __name__ == '__main__':
    UberCLI().main()
