#  smtp encapsulation connection between server.

import socket
import sys
from threading import*

host= "127.0.0.1"
port= 50007
users=[]
for i in users:
    user= input('Enter your user name:')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b' Test Message ')
    data = s.recv(1024)
print('Other Message', repr(data))
    
    
    
    






   
            



    

        
    

    






