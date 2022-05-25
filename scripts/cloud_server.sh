#!/usr/bin/env bash

## Traffic going to the internet
route add default gw 172.48.48.49

## Save the iptables rules
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6

sudo apt update
sudo apt install -y wireguard python3-pip
cd /home/vagrant/overlay_manager
pip3 install requests

curl http://meshmash.vikaa.fi:49177/devices/$2/token -H "x-api-key: 591Bc13b7129eE1f8eF3F4A7BAf7B7EB" -H "Content-Type: application/json"  -o token.txt




sudo python3 main.py $1 $2 $3 


