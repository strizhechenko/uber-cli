#!/usr/bin/env python

""" Example: ./addr2geo.py "Vostochnaya 33, Yekaterinburg" """

from sys import argv
from pygeocoder import Geocoder


def addr2geo(addr):
    return Geocoder().geocode(addr).coordinates

if __name__ == '__main__':
    addr = " ".join(argv[1:])
    print addr2geo(addr)
