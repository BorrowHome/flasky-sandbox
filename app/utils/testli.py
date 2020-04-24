import nmap

nm = nmap.PortScanner(nmap_search_path=('nmap', r"D:\nmap\nmap-7.80\nmap.exe"))

nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,8899')
a = nm.command_line()
print(a)
