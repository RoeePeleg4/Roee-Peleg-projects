import socket , select

MAX_MSG_LENGTH = 1024 #max length of the msg from client
SERVER_PORT = 5555 #the port of the server 
SERVER_IP = "0.0.0.0" #The ips that the server listens to 

# printing the current sockets that are connected
def print_client_sockets(client_sockets):
     for c in client_sockets:
         print("\t", c.getpeername()) 

def main():
    print("server is up and running...")
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM) #explanation in tcp example
    server_socket.bind((SERVER_IP , SERVER_PORT)) #explanation in tcp example
    server_socket.listen() #explanation in tcp example
    print("listening for clients")
    client_sockets = []
    messages_to_send = [] #contains socketObject and a string of data
    while True:
        ready_to_read , ready_to_write , in_error = select.select([server_socket] + client_sockets , [] , []) #explanation in selectFunc
        isNewClient = False
        #if the socket of the server is a new one we need to accept it, and recive info from it  
        # if the socket of the server is an old one we need to recive info from it
        for current_socket in ready_to_read: #itarates over the list of sockets
            if current_socket is server_socket: #check if the socket the we check is the same as the one that recived in the server socket if it that means it is a new socket in the server
                client_socket , client_address = current_socket.accept() #accept to the new socket
                print(f"new client joined! with the address of {client_address}")
                client_sockets.append(client_socket) #add the new socket to the list of sockets
                isNewClient = True
                print_client_sockets(client_sockets)
            else: # how does it work?
                print("new data from client")
                #try in order to handle with forcibly close of cmd
                try:
                    data = current_socket.recv(MAX_MSG_LENGTH).decode() # reciving the message
                except:
                    client_sockets.remove(current_socket)
                    client_socket.close()
                    print ("cmd window close and we closed connection with the client")
                    print (client_sockets)
                    break
                if data == "":
                    print( "Connection closed" , )
                    client_sockets.remove(current_socket)
                    messages_to_send.append((current_socket , data)) # append the info to send in an array
                    client_socket.close() # inorder the user to close connection
                    print_client_sockets(client_sockets)
                else: 
                    print(data)
                    current_socket.send(data.encode())
        # send the data only to avilable clients
        for msg in messages_to_send:
            current_socket , data = msg
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messages_to_send.remove(msg)

if __name__ == "__main__":
    main()


# Q: I dont know if 2 clients try to reach the server at the same time one will wait? A: they will both be in qeue and the code will handle each at diffrent iteration
# first the client sends request to access the server, all the requests are in que, i think, and it will handle it in the few nexts.
# the request to access and the send of message are diffrent actions
# I think the ready_to_read contain only one element at the time