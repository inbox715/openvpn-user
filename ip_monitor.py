import subprocess
from time import sleep
import os
import threading
import math
import cherrypy

c_dir = os.path.dirname(os.path.abspath(__file__)) + '/'

try:
    f = os.popen('ifconfig')
    server_ip=f.read()
    server_ip = server_ip.split("inet ")[1]
    server_ip = server_ip.split(" ")[0]
except :
    server_ip= "127.0.0.1"

cherrypy.config.update({
    'server.socket_host':server_ip, 
    'server.socket_port':31223,
    'log.screen' : False,
 })





def convert_size(size_bytes):
    size_bytes= int (size_bytes)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])







output=''
def run():
    global output
    your_command= ["tcpdump","-i" ,"ens3","-Q","in","-q" , "dst" ," vps-2ce94891.vps.ovh.net"]
    output = subprocess.Popen(your_command, stdout=subprocess.PIPE ,universal_newlines=True)

th = threading.Thread(target=run, args=())
th.start()




sleep(1)



size=0
ip_dic={}
def cal():
    global size
    global output
    global ip_dic
    while True:

        try:
            a= output.stdout.readline().split(" ")

            url = ".".join(a[2].split(".")[:-1])

            if url in ip_dic:
                ip_dic[url]=ip_dic[url] + int (a[len(a)-1])
            else:
                ip_dic[url]= int (a[len(a)-1])
        except :
            pass


th = threading.Thread(target=cal, args=())
th.start()








class PINKO(object):
    @cherrypy.expose
    def index(self):
        table='''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>user info!</title>
  <link rel="stylesheet" href="static/css/bootstrap.min.css">
  <link rel="stylesheet" href="static/css/style.css">
</head>
<body>

        
        <table class="table table-sm table-dark">
            <thead>

                <tr>
                <th scope="col">ip</th>
                <th scope="col">data</th>
                </tr>
            </thead>
             <tbody>
                %info%
                 </tbody>
                </table>
</body>
</html>
                
                
                '''


        ip_list=sorted(ip_dic.items(), key=lambda x: x[1], reverse=True)

        info=""
        for ip in ip_list:
            if ip[1] >0 :
                info = info+'''<tr>
                                <td>'''+str(ip[0])+'''</td>
                                <td>'''+str(convert_size(ip[1]))+'''</td>
                            </tr>'''

        return table.replace("%info%",info)


conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': c_dir
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    }
}

cherrypy.quickstart(PINKO(), '/', conf)









