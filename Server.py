import socket
import select

HEADER_LENGTH = 10

HOST = "127.0.0.1"
PORT = 50007

#Create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Reuse the port if already exist and in-use
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Bind with the given IP and port number
server_socket.bind((HOST, PORT))
#Listen to connections
server_socket.listen()
#List of sockets for select.select
sockets_list = [server_socket]
#List of connected clients - socket as key, user is the header and name is the data
clients = {}

#Function that recieves messages
def receive(client_socket):
    try:
        #Receiving the header that contains the message length
        message_header = client_socket.recv(HEADER_LENGTH)
        #Received no data, close the connection
        if not len(message_header):
            return False
        #Convert the length to integer
        message_length = int(message_header.decode('utf-8').strip())
        #Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}    
    except:
        #Something went wrong with the client, where it closes
        return False
while True:
    #Blocking call, code execute wait and notify any action that occurs 
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    #
    for notified_socket in read_sockets:
        #If notified socket is ser socket, there is a new connection
        if notified_socket == server_socket:
            #accept the new connection with new socket, client socket
            #connected uniquely
            client_socket, client_address = server_socket.accept()
            #Client should send the name and receive it
            user = receive(client_socket)
            if user is False:
                continue
            #Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            #Save username and username header
            clients[client_socket] = user
            print('Connected by {} at (\'{}\',{})'.format(user['data'].decode('utf-8'),
            *client_address))
        #Existing socket has a message
        else:
            #Receive the message
            message = receive(notified_socket)
            #if the message not receive, disconnect
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]
                ['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            #Get user by notified socket to see who sent the message
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            #Looping through connected clients and broadcast messages
            for client_socket in clients:
                #Don't send it to the sender
                if client_socket != notified_socket:
                    #Send user and messager with their headers
                    client_socket.send(user['header'] + user['data'] + message['header'])