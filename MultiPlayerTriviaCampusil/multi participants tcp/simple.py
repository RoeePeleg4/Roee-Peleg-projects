import socket
#client that sends info to the server and getting it back
my_socket = socket.socket (socket.AF_INET , socket.SOCK_STREAM) #creating a socket (Ip protocol , Tcp protocol) in the client side
my_socket.connect(("127.0.0.1" , 5555)) # the (Ip , Port) of the serve simular to 3rd line
while True:
    a = 1

print("closing socket")
my_socket.close() #closes the connection