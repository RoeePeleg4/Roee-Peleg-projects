import socket

server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM) #creating a socket (Ip protocol , Tcp protocol) in the server side
server_socket.bind(("0.0.0.0" , 8820)) #determaines to what IP adress and Port the server listen to, IP:"0.0.0.0" means all IPs
server_socket.listen() #make the server to start listen
print("server is up and running ")
(client_socket , client_adress) = server_socket.accept() #the function is accepting the client's request and saves his adress and his socket, it's waiting for a connection from the client, only after the accept a connection is established. the function is blocking so the code isn't running untill its finished
print("client connected")
while True: # the while is occuring while the server connect to one client
    data = client_socket.recv(1024).decode() #gets the data from the client in binary and decode it (via UTF-8 I think)
    print(f"client send {data}")
    #if data == "Bye": # inteded to face a Bye recv that will disconnect the client
    #    data = " "
    if (data == "Quit"):
        print("closing client socket now...")
        client_socket.send("Bye".encode())
        break
    data = data.upper() + "!!!"
    client_socket.send(data.encode()) # the server sends back data to the client. client's recive method and send are the same and uses the client_socket
client_socket.close() #close connection with the client
server_socket.close() #close server connection
# client_socket our connection with an individual client, sending back info, receving it etc
# server_socket socket that new clients connect to
