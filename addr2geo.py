#!/usr/bin/env python
# coding: utf-8

""" Example: ./addr2geo.py "Vostochnaya 33, Yekaterinburg" """

from sys import argv
from sqlite3 import Connection
from pygeocoder import Geocoder


def addr2geo(addr, cache):
    return addr2geo_cache(addr, cache) or addr2geo_api(addr, cache)


def cache_init(cache):
    check = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='points';"
    create = "create table points (id varchar, lat double, lng double);"
    if not cache.execute(check).next()[0]:
        cache.execute(create)


def addr2geo_cache(addr, cache):
    cache_init(cache)
    select = "SELECT lat, lng FROM points WHERE id='{0}';".format(addr)
    for lat, lng in cache.execute(select):
        return lat, lng


def addr2geo_api(addr, cache):
    lat, lng = Geocoder().geocode(addr).coordinates
    q = "INSERT INTO points VALUES ('{0}', {1}, {2});".format(addr, lat, lng)
    cache.execute(q)
    return addr2geo_cache(addr, cache)


def main():
    with Connection('points.db') as cache:
        addr = " ".join(argv[1:])
        print addr2geo(addr, cache)

if __name__ == '__main__':
    main()
