#!/bin/bash  
echo "This is a shell script" 
echo "try install cherrypy"


sudo apt -y install net-tools

sudo apt -y install python3-pip
sudo pip3 install cherrypy

sudo apt -y install git



sudo rm -rf openvpn-user-list-multiserver
git clone https://github.com/inbox715/openvpn-user-list-multiserver.git


sudo ufw allow 31221
sudo ufw allow 31222


python3 ./openvpn-user-list-multiserver/user.py &
python3 ./openvpn-user-list-multiserver/server.py &

