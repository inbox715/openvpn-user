import telnetlib
from datetime import datetime
import cherrypy
import os 
import math


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

def convert_size(size_bytes):
    size_bytes= int (size_bytes)
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


info="""
OpenVPN CLIENT LIST
Updated,Sun Dec 13 04:42:23 2020
Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since
blue,95.38.115.150:16634,11275576,74247571,Sun Dec 13 03:15:52 2020
blue,110.39.160.10:40246,18580590,331113355,Sun Dec 13 03:17:46 2020
blue,5.123.62.13:40695,409190,2252703,Sun Dec 13 03:47:29 2020
blue,2.50.108.15:59787,184342,304956,Sun Dec 13 03:19:01 2020
ROUTING TABLE
Virtual Address,Common Name,Real Address,Last Ref
10.8.0.2,blue,95.38.115.150:16634,Sun Dec 13 04:42:22 2020
10.8.0.3,blue,110.39.160.10:40246,Sun Dec 13 04:39:36 2020
10.8.0.6,blue,5.123.62.13:40695,Sun Dec 13 04:42:17 2020
10.8.0.5,blue,2.50.108.15:59787,Sun Dec 13 04:39:50 2020
GLOBAL STATS
Max bcast/mcast queue length,6
END"""






user_list = info.split("Connected Since\n")[1]
user_list = user_list.split("\nROUTING TABLE")[0]
user_list = user_list.split("\n")



name_list=[]
address_list=[]
download_list=[]
upload_list=[]
connect_time_list=[]


for user in user_list:
    user_parameter = user.split(",")
    name_list.append(user_parameter[0])
    address_list.append(user_parameter[1])
    download_list.append(convert_size(user_parameter[2]))
    upload_list.append(convert_size(user_parameter[3]))

    fmt = '%a %b %d %H:%M:%S %Y'
    now_time = datetime.now()
    d1 = datetime.strptime(user_parameter[4], fmt)
    d2 = datetime.strptime(now_time.strftime(fmt), fmt)
    connect_time_list.append(str((d2-d1)))


    print(user)


print ("0")



class PINK(object):
    @cherrypy.expose
    def index(self):
        page = open("index.html").read()

        name_table=''
        for table_row in range(len(name_list)):
            name_table=name_table+'<tr><th scope="row">'+str(table_row+1)+'</th>'
            name_table=name_table+"<td>"+name_list[table_row]+"</td>"
            name_table=name_table+"<td>"+address_list[table_row]+"</td>"
            name_table=name_table+"<td>"+download_list[table_row]+"</td>"
            name_table=name_table+"<td>"+upload_list[table_row]+"</td>"
            name_table=name_table+"<td>"+connect_time_list[table_row]+"</td>"
            name_table=name_table+'</tr>'

        




        page=page.replace("%info%", name_table)


        return page





cwd = os.getcwd()
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': cwd
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './static'
    }
}

cherrypy.quickstart(PINK(), '/', conf)





import telnetlib
import os


f = os.popen('ifconfig')
your_ip=f.read()
your_ip = your_ip.split("inet ")[1]
your_ip = your_ip.split(" ")[0]


host = "127.0.0.1"
port = 5555
timeout = 100

with telnetlib.Telnet(host, port, timeout) as session:
    session.write(b"status\n")
    info = session.read_until(b"END").decode("utf-8")

    info.split
    print (info)













