import cherrypy
import os 
import telnetlib


try:
    f = os.popen('ifconfig')
    server_ip=f.read()
    server_ip = server_ip.split("inet ")[1]
    server_ip = server_ip.split(" ")[0]
except :
    server_ip= "127.0.0.1"

cherrypy.config.update({
    'server.socket_host':server_ip, 
    'server.socket_port':31221,
    'log.screen' : False,
 })



class PINK(object):
    @cherrypy.expose
    def index(self):


        host = "127.0.0.1" # set in open vpn config file
        port = 5555 # set in open vpn config file
        timeout = 100
        with telnetlib.Telnet(host, port, timeout) as session:
            session.write(b"status\n")
            info = session.read_until(b"END").decode("utf-8")

        return info

c_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': c_dir
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir':'./static'
    }
}

cherrypy.quickstart(PINK(), '/', conf)

