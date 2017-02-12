#!/bin/bash
route add default gw 192.168.7.1
sleep 1
service ntp stop
ntpdate -s us.pool.ntp.org
service ntp start
