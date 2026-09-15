import nmap
nm = nmap.PortScanner()
ip="192.168.1.1"
nm.scan(ip, '22-443')
nm.command_line()
nm.all_hosts()
print(nm[ip].hostname())
print(nm[ip].state())
print(nm[ip].all_protocols())
print(nm[ip]['tcp'].keys())


#for host in nm.all_hosts():
  #  print('----------------------------------------------------')
  #  print('Host : %s (%s)' % (host, nm[host].hostname()))
 # #  print('State : %s' % nm[host].state())
  #  for proto in nm[host].all_protocols():
  #      print('----------')
  #      print('Protocol : %s' % proto)
  #      lport = nm[host][proto].keys()
  #      lport.sort()
  #      for port in lport:
   #         print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
            
            
#nma = nmap.PortScannerAsync()
host=ip+"/24"
nm.scan(hosts=host, arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
print(hosts_list)
for host, status in hosts_list:
    print(host,status)

#for host, status in hosts_list:
#    nm.scan(host, '22-40043')


for host,status in hosts_list:
     print('----------------------------------------------------')
     print('Host : %s ' % (host))
     print('State : %s' % (status))
     nm.scan(host)
     for proto in nm[host].all_protocols():
         print('----------')
         print('Protocol : %s' % proto)
         print(nm[host][proto])
         lport = nm[host][proto].keys()
         print(lport)
         sorted(lport)
         for port in lport:
             print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))