import socket
IP = "0.0.0.0"
PORT = 8821 

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) 
sock.bind((IP , PORT))
while True:
    client_message , client_address = sock.recvfrom(1024)
    data = client_message.decode()
    print (f"client send: {data}")
    if (data.lower() == "exit"):
        response = "exit"
        sock.sendto(response.encode() , client_address)
        break 
    response = "hello " + data
    sock.sendto(response.encode() , client_address)
sock.close()