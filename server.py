import telnetlib
from datetime import datetime
import cherrypy
import os 
import math
import requests


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
    'server.socket_port':31222,
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

















class PINK(object):
    @cherrypy.expose
    def index(self,**param):

        table_sample = """<table class="table table-sm table-dark">
        
            <thead>
                <tr>
                    <th scope="col">%server%</th>
                </tr>

                <tr>
                <th scope="col">#</th>
                <th scope="col">name</th>
                <th scope="col">address</th>
                <th scope="col">download</th>
                <th scope="col">upload</th>
                <th scope="col">connect_time</th>
                </tr>
            </thead>
            <tbody>
            %info% """
        tables=[]
        page = open(c_dir+"index.html").read()

        if len (param) == 0:
            return "hi boss"


        servers= param['sub'].split(",")
        for server in servers:
            try:
                url = 'http://'+server+":31221"
                data = requests.get(url,timeout=5).text



                user_list = data
                user_list = user_list.split("Connected Since\r\n")[1]
                user_list = user_list.split("\r\nROUTING TABLE")[0]
                user_list = user_list.split("\r\n")

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


                name_table=''
                for table_row in range(len(name_list)):
                    name_table=name_table+'<tr><th scope="row">'+str(table_row+1)+'</th>'
                    name_table=name_table+"<td>"+name_list[table_row]+"</td>"
                    name_table=name_table+"<td>"+address_list[table_row]+"</td>"
                    name_table=name_table+"<td>"+download_list[table_row]+"</td>"
                    name_table=name_table+"<td>"+upload_list[table_row]+"</td>"
                    name_table=name_table+"<td>"+connect_time_list[table_row]+"</td>"
                    name_table=name_table+'</tr>'

                table_sample=table_sample.replace("%server%", server)
                tables.append(table_sample.replace("%info%", name_table))
            except :

                tables.append('<div class="alert alert-danger" role="alert"> Error in '+server+'</div>')


                

                

        
        html_table=''
        for table in tables:
            html_table=html_table+table+"<br>"

        page=page.replace("%tables%", html_table)


        return page




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

cherrypy.quickstart(PINK(), '/', conf)





# import telnetlib
# import os


# f = os.popen('ifconfig')
# your_ip=f.read()
# your_ip = your_ip.split("inet ")[1]
# your_ip = your_ip.split(" ")[0]


# host = "127.0.0.1"
# port = 5555
# timeout = 100

# with telnetlib.Telnet(host, port, timeout) as session:
#     session.write(b"status\n")
#     info = session.read_until(b"END").decode("utf-8")

#     info.split
#     print (info)













