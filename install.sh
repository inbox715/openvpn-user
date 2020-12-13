#!/bin/bash  
echo "This is a shell script" 
echo "try install cherrypy"

sudo apt install python3-pip
sudo pip3 install cherrypy

sudo apt install git


sudo rm -rf openvpn-user
git clone https://github.com/inbox715/openvpn-user 

nohup python3 ./openvpn-user/user.py &
nohup python3 ./openvpn-user/server.py &
