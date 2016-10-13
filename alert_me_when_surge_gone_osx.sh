#!/bin/bash

. env/bin/activate

date +%H:%M 
while ! ./is_uber_cheap.py "${DST:-home}"; do
	sleep "${INTERVAL:-60}"
	date +%H:%M
done

for i in {1..4}; do 
	afplay /System/Library/Sounds/Ping.aiff
done
