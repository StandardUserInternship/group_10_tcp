import socket
from threading import*
import sys




#ip address as a loop back and a port number

host = "127.0.0.1" #Local host
port = 50007 #port number

#Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((host,port))
    #Listening for an incoming message
    s.listen(5)

    clients = []
    nicknames = []
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print('Test message')
        print('Message: other message')

        while True:
            data =conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


          

          

          
            









    
            





   




#create a connection to enable client to connect to you the server

    
   
