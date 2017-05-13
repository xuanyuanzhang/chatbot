import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('100.8.239.245',5001))
    s.sendall("hi from James")
    msg = s.recv(1024)
    print msg

except:
    raise
