import nmap

# 测试用，觉得应该有用。使用nmap这个工具，扫描端口，自动获得网络中支持onvif协议的ipc
nm = nmap.PortScanner(nmap_search_path=('nmap', r"D:\nmap\nmap-7.80\nmap.exe"))

nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,8899')
a = nm.command_line()
print(a)
