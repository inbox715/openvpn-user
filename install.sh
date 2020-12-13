#!/bin/bash  
echo "This is a shell script" 
echo "try install cherrypy"

sudo apt install python3-pip
sudo pip3 install cherrypy

sudo apt install git



sudo rm -rf openvpn-user
git clone https://github.com/inbox715/openvpn-user 


allow ufw allow 31221
allow ufw allow 31222


python3 ./openvpn-user/user.py &
python3 ./openvpn-user/server.py &

