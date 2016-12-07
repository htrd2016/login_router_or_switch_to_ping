#username password cisco_ip zabbix_server_ip time_interval(ms) config_file
nohup python ./pingByTelnetSwitch.py test test 192.168.103.230 192.168.103.112 500 switch_telnet_config.ini > /dev/null 2> log &
nohup python ./pingBySSHRouter.py test test 100.195.96.254 192.168.103.112 500 router_ssh_config.ini > /dev/null 2> log &
