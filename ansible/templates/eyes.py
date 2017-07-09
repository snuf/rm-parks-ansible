#!/usr/bin/python
import random
import sys
import math
import requests
import json
from time import sleep

# US
long_max=50
long_min=25
latt_max=-130
latt_min=-70

def check_float(n):
    try:
        float(n)
        return n
    except ValueError:
        return 0.3

def get_randoms():
    latt_mid=random.randint(25, 50)
    long_mid=random.randint(-130, -70)
    dev=random.sample([-5, 5],  1)
    long_end=long_mid-dev[0]
    latt_end=latt_mid-dev[0]
    return [long_mid, long_end, latt_mid, latt_end]

def lode(server, interval):
    try:
        while True:
            lon1, lon2, lat1, lat2 = get_randoms()
            url="%sparks/within?lat1=%s&lon1=%s&lat2=%s&lon2=%s" % (server, lat1, lon1, lat2, lon2)
            r = requests.get(url)
            print r.text
            sleep(interval)
    except Exception, e:
        print "Exception: %s" % (e)

server=sys.argv[1]
interval=check_float(sys.argv[2])

while True:
    lode(server, interval)
