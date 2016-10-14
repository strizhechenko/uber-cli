#!/bin/bash

cd /root/uber_surge_alerter
. env.sh
python influxdb_agent.py 
