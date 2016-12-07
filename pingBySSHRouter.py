import paramiko
import os
import sys
import time

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

def get_ping_percent(remote_conn, ip):
    remote_conn.send("ping "+ip+"\n")
    data = ""
    while(data.find(">") == -1):
       data = data + remote_conn.recv(5000)

    indexStart = data.find("Success rate is ")
    indexEnd = data.find(" percent");
    if (indexStart>0 and indexEnd>0):
        #print(indexStart)
        #print(indexEnd)
        indexStart+=16
        per = data[indexStart:indexEnd]
        #print(per.strip())
        return per.strip()
        #os.system("zabbix_sender -z " + zabbixserverip + " -s \""+hostname+"\" -k sender.ping.mc -o "+per.strip())

    return 0

if __name__ == '__main__':
    ret_arr = read_config(config_file)
    print print_conf(ret_arr)
    
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(serverip, username=user, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % serverip

    remote_conn = remote_conn_pre.invoke_shell()

    output = ""
    while(output.find(">") == -1):
       output = output + remote_conn.recv(5000)

    while True:
        for host in ret_arr:
            if(host is None):
               continue

            print host
            percent = get_ping_percent(remote_conn, host[0])
            send_to_server(zabbixserverip, host[1], host[2], percent)
        time.sleep(0.001*time_interval)

    remote_conn_pre.close()
