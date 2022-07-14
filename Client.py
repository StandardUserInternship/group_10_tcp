import socket 
import select
import errno
import sys

HEADER_LENGTH = 10

HOST = "127.0.0.1"
PORT = 50007
my_username = input("Username: ")

#Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect the socket
client_socket.connect((HOST, PORT))
#Used so that recv() doesn't get blocked
client_socket.setblocking(False)
#Encode the username and header to bytes, header counts number of bytes
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
#Send the username and header
client_socket.send(username_header + username)

print(f"< Server > Welcome {my_username}")

while True:
    #User input message
    message = input(f'< {my_username} > ')
    #If there is a message
    if message:
        #Encode the message to bytes and header 
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        #Send the message
        client_socket.send(message_header + message)
    try:
        #Going through the recieved messages
        while True:
            #Recieve the username length
            username_header = client_socket.recv(HEADER_LENGTH)
            #If no data has been received, close the connection!
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            #Convert to an int 
            username_length = int(username_header.decode('utf-8').strip())
            #Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            #Decode the message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            #Print the message
            print(f'{username} > {message}')
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
        continue
    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()

