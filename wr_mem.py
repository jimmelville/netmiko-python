from netmiko import ConnectHandler
from netmiko import ssh_exception
from netaddr import IPNetwork, IPAddress


LONDON_Old_Network = IPNetwork("192.168.0.0/24")
YORK_Old_Network = IPNetwork("192.168.1.0/24")
ABERDEEN_Old_Network = IPNetwork("192.168.2.0/24")
SHEFFIELD_Old_Network = IPNetwork("192.168.3.0/24")

LONDON_New_Network = IPNetwork("10.0.0.0/16")
YORK_New_Network = IPNetwork("10.1.0.0/16")
ABERDEEN_New_Network = IPNetwork("10.2.0.0/16")
SHEFFIELD_New_Network = IPNetwork("10.3.0.0/16")


def get_site_name(switch_ip):
    if switch_ip in in LONDON_Old_Network:
            return "LONDON"
    elif switch_ip in LONDON_New_Network:
            return "LONDON"
    elif switch_ip in YORK_Old_Network:
            return "YORK"
    elif switch_ip in YORK_New_Network:
            return "YORK"
    elif switch_ip in ABERDEEN_Old_Network:
            return "ABERDEEN"
    elif switch_ip in ABERDEEN_New_Network:
            return "ABERDEEN"
    elif switch_ip in SHEFFIELD_Old_Network:
            return "SHEFFIELD"
    elif switch_ip in SHEFFIELD_New_Network:
            return "SHEFFIELD"
    else:
            return "Unknown Site"
	
switch_ips = ['10.0.0.1',
'10.1.0.1',
'10.2.0.1',
'10.3.0.1',]

for switch_ip in switch_ips:
    switch = {
             'device_type': 'cisco_ios',
             'ip': switch_ip,
             'username': 'cisco',
             'password': 'cisco',
             'secret': 'enable'
             }
    site_name = get_site_name(switch_ip)
    try:
        net_connect = ConnectHandler(**switch)
        print(net_connect)
    except ssh_exception.AuthenticationException:
        print("Wrong Credentials for "+ site_name + " switch "+switch_ip)
    except ssh_exception.NetMikoTimeoutException:
        print ("Timed out when connecting to "+ site_name + " switch "+switch_ip)
    except ssh_exception.SSHException:
        print ("Other SSH issue for "+ site_name + " switch "+switch_ip)    
    else:
        print (site_name+" Switch "+switch_ip)
        net_connect.enable()
        wr_mem = net_connect.send_command("wr mem", delay_factor = 1)
        print (wr_mem)
        print()
        net_connect.disconnect()
