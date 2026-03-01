import socket
SERVER_PORT = 8821
SERVER_IP = "127.0.0.1" #local host

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) #creating a socket that is via udp protocol (SOCK_DGRAM)
sock.sendto("Roee".encode() , (SERVER_IP , SERVER_PORT)) #sends a message to the server, the port and ip are the server ones
#the diffrent from TCP is that there is no need for connection request and that the socket is open only when the messages are being sent and not always (the socket between the client -> server (Im not sure if both))
response , remoteAdress = sock.recvfrom(1024) # reciving a message from the server
# unlike tcp because the connection in not always open there is a need for the ip adress of the sender to know who sent the message
data = response.decode() #get the message and decode it from binary
print (f" server sent: {data}")
sock.close()
#I think that even though the connection is not always open we need to close it inorder to close it permenetly

#sending messages - TCP - send, UDP - sendto
#reciving messages - TCP - recv, UDP - recvfrom
#connecting - TCP - connect - UDP - no need
#creating socket - TCP - socket.SOCK_STREAM, UDP - socket.SOCK_DGRAM
