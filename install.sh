  
#!/bin/bash  
echo "This is a shell script" 
echo "try install cherrypy"


apt -y install net-tools

apt -y install python3-pip
pip3 install cherrypy

apt -y install git



rm -rf openvpn-user-list-multiserver
git clone https://github.com/inbox715/openvpn-user-list-multiserver.git


ufw allow 31221
ufw allow 31222
ufw allow 22
ufw allow 443
ufw --force enable

python3 ./openvpn-user-list-multiserver/user.py &
python3 ./openvpn-user-list-multiserver/server.py &