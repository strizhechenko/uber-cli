# coding=utf-8
import json
import datetime
import requests


class BaseWriter(object):
    def __init__(self, options):
        self.options = options

    def write(self, price, places):
        pass

    def header(self):
        pass


class PlainWriter(BaseWriter):
    def write(self, price, places):
        product = price[0]
        print("{0} : {1:12} : {2:5} : {3:5}".format(
            datetime.datetime.now(),
            product['display_name'],
            product['low_estimate'],
            product['high_estimate']))

    def header(self):
        print("{0:26} : {1:12} : {2:5} : {3:5}".format("Time", "Product", "Min", "Max"))


class DictWriter(BaseWriter):
    def write(self, price, places):
        print(json.dumps(price, indent=4))


class InfluxWriter(BaseWriter):
    def write(self, price, places):
        assert self.options.influxdb, "Please, supply --influxdb-url <url>"
        product = price[0]
        for key in ('low_estimate', 'high_estimate'):
            data = "{0},src={1},dst={2} value={3}".format(
                key, places['src'].addr, places['dst'].addr, product.get(key))
            print(self.options.influxdb, '-d', data)
            try:
                requests.post(self.options.influxdb, data)
            except requests.exceptions.ConnectionError as err:
                print(err)
