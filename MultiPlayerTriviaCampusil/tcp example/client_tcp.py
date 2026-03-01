import socket
#client that sends info to the server and getting it back
my_socket = socket.socket (socket.AF_INET , socket.SOCK_STREAM) #creating a socket (Ip protocol , Tcp protocol) in the client side
my_socket.connect(("10.0.0.16" , 8820)) # the (Ip , Port) of the serve simular to 3rd line, and connect to the server
while True:
    msg = str(input("what do U wanna send to the server? "))
    my_socket.send(msg.encode()) # the client sends a message to the server, encoded to binary
    data = my_socket.recv(1024).decode() #recive the message from the server and decode it from binary
    print(f"the server sent {data}")
    if (data == "Bye"):
        break

print("closing socket")
my_socket.close() #closes the connection