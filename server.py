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

        <button type="button" class="btn btn-dark rounded-0">%server%</button>


            <thead>

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




        import threading


        ip_info={}
        error_list=[]

        def get_url(ip):
            try:
                url = 'http://'+ip+":31221"
                data = requests.get(url,timeout=5).text
                ip_info[ip]=data
            except :
                tables.append('<div class="alert alert-danger" role="alert"> Error in '+ip+'</div>')
                error_list.append('<div class="alert alert-danger" role="alert"> Error in '+ip+'</div>')


        t_list=[]
        for server in servers:
            t = threading.Thread(target=get_url, args = (server,))
            t.start()
            t_list.append(t)

        for t in t_list:
            t.join()


        number_of_user=0

        for server in ip_info:
            # url = 'http://'+server+":31221"
            # data = requests.get(url,timeout=5).text



            user_list = ip_info[server]
            user_list = user_list.split("Connected Since\r\n")[1]
            user_list = user_list.split("\r\nROUTING TABLE")[0]
            user_list = user_list.split("\r\n")

            if user_list[0]=='ROUTING TABLE': #for detect no user
                table_temp=table_sample.replace("%server%", server)

                tables.append('''
                <table class="table table-sm table-dark">
                <div class="alert alert-warning" role="alert"> no user '''+server+''' </div>
                <tbody>
                ''')

            else:
                name_list=[]
                address_list=[]
                download_list=[]
                upload_list=[]
                connect_time_list=[]

                for user in user_list:
                    number_of_user = number_of_user + 1
                    user_parameter = user.split(",")
                    name_list.append(user_parameter[0])
                    address_list.append(user_parameter[1])
                    upload_list.append(convert_size(user_parameter[2]))
                    download_list.append(convert_size(user_parameter[3]))

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

                table_temp=table_sample.replace("%server%", server)
                tables.append(table_temp.replace("%info%", name_table))



                

        if 'n' in param and param['n']=='1':

            html_table=''
            for table in error_list:
                html_table=html_table+table+"<br>"
            page=page.replace("%tables%", html_table)
            if error_list.__len__() == 0:
                page=page.replace("%tables%", "")

            return  '<p id="user_no_only">' + str (number_of_user) +'</p>' +page       

        else:   
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













