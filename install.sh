#!/bin/bash  
echo "This is a shell script" 
echo "try install cherrypy"

sudo apt install python3-pip
sudo pip3 install cherrypy

if [ ! -d py ] 
then
    mkdir -p py
fi

if [ ! -d py/static ] 
then
    mkdir -p py/static
fi

if [ ! -d py/static/css ] 
then
    mkdir -p py/static/css
fi

if [ ! -d py/static/js ] 
then
    mkdir -p py/static/js
fi


echo "make test folder"


git clone https://github.com/inbox715/openvpn-user 
