import paramiko
import os

import sys

user = sys.argv[1]
password = sys.argv[2]
serverip =  sys.argv[3]
iptoping = sys.argv[4]
zabbixserverip = sys.argv[5]
hostname = sys.argv[6]

def ping(remote_conn, ip):
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
        print(per.strip())
        os.system("zabbix_sender -z " + zabbixserverip + " -s \""+hostname+"\" -k sender.ping.mc -o "+per.strip())

if __name__ == '__main__':
    #ip = '10.195.96.254'
    #username = 'admin'
    #password = 'cisco123'

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(serverip, username=user, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % serverip

    remote_conn = remote_conn_pre.invoke_shell()

    output = ""
    while(output.find(">") == -1):
       output = output + remote_conn.recv(5000)

    while True:
        ping( remote_conn, iptoping)
    time.sleep(0.5)
 
    print output

