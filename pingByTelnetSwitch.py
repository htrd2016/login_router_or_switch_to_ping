import telnetlib
import time
import os
import sys

user = sys.argv[1]
password = sys.argv[2]
serverip =  sys.argv[3]
zabbixserverip = sys.argv[4]

time_interval = int(sys.argv[5])
config_file = sys.argv[6]

def read_config(file_name):
    file_object = open(file_name)
    ret_arr = []
    try:
        lines = file_object.readlines()
        for line in lines:
            line = line.replace('\n','')
            if(len(line)>0 and line[0] == '#'):
                continue
            line_arr = line.split('|', 2)
            if(len(line_arr)<=1):
                continue
            ret_arr.append(line_arr)
    finally:
        file_object.close()

    return ret_arr

def print_conf(arr):
    for line in arr:
       print line

def send_to_server(zabbixserverip, hostname, key, data):
#    print("zabbix_sender -z "+ zabbixserverip +" -s "+hostname+" -k "+key+" -o "+data)
    os.system("zabbix_sender -z "+ zabbixserverip +" -s "+hostname+" -k "+key+" -o "+data)


def get_ping_percent(tn, ip_to_ping):
    try:
        tn.write("ping " + ip_to_ping + "\r\n")
        data = tn.read_until(">")
        indexStart = data.find("Success rate is ")
        indexEnd = data.find(" percent");
        if (indexStart>0 and indexEnd>0):
            #print(indexStart)
            #print(indexEnd)
            indexStart+=16
            per = data[indexStart:indexEnd]
#            print(per.strip())
            #os.system("zabbix_sender -z "+ zabbixserverip +" -s \""+hostname+"\" -k sender.ping.mc -o "+per.strip())
            return per.strip()
    except Exception,e:  
         print Exception,":",e
         return 0
    return 0

        
if __name__ == "__main__":
    ret_arr = read_config(config_file)
    print print_conf(ret_arr)

    tn = telnetlib.Telnet(serverip)

    tn.read_until("Username: ")
    tn.write(user + "\n")

    if password:
        print(tn.read_until("Password: "))
        tn.write(password + "\n")
#       print(password)
        #print(tn.read_all())
        tn.read_until(">")
   
    while True: 
        for host in ret_arr:
          if(host is None):
              continue

          print host
          percent = get_ping_percent(tn, host[0])
          send_to_server(zabbixserverip, host[1], host[2], percent)
 #        print percent
        time.sleep(0.001*time_interval)
    tn.write("exit\n")
    print(tn.read_all()) 

