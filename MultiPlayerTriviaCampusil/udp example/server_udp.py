import socket
IP = "0.0.0.0" #that means that it listens to all ip that address the server
PORT = 8821 #the port that the server listens to 

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) # creating a new socket
sock.bind((IP , PORT)) # connecting to the IP and PORT that enables it to start listening
# the server answer in the same port as created so no need for 2 sockets
# there is no need for listen nor accept because the information is going through the socket that the client opened
# in udp there is no socket for the client because the is no "always on" connection with the client
client_message , client_address = sock.recvfrom(1024) # reciving info from the client 
data = client_message.decode() #decode the message from binary
print (f"client send: {data}")
response = "hello " + data
sock.sendto(response.encode() , client_address) #sending back to client
sock.close() # closing socket