#!/usr/bin/env bash

## Traffic going to the internet
route add default gw 10.1.0.1

## Save the iptables rules
iptables-save > /etc/iptables/rules.v4
ip6tables-save > /etc/iptables/rules.v6



## Install app
cd /home/vagrant/client_app
npm install

cat << EOF > config.json
{
  "server_ip": "172.48.48.51",
  "server_port": "8080",
  "log_file": "/var/log/client.log"
}
EOF

## Install wireguard manager software
sudo apt update
sudo apt install -y wireguard python3-pip
cd /home/vagrant/overlay_manager
pip3 install requests

echo $4 > token.txt
sudo python3 main.py $1 $2 $3 

