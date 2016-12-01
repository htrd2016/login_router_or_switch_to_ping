#username password cisco_ip ip_to_ping zabbix_server_ip zb_host_name
#nohup python ./pingByTelnetSwitch.py test test 192.168.103.252 192.168.103.51 192.168.103.112 > /dev/null 2>log &
nohup python ./pingByTelnetSwitch.py test test123 192.168.103.230 192.168.103.51 192.168.103.112 "cisco switch WS-C3750X-48" > /dev/null 2> log &
nohup python ./pingBySSHRouter.py test test 100.195.96.254 192.168.103.51 192.168.103.112 "cisco router" > /dev/null 2> log &
