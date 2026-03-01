import socket
SERVER_PORT = 8821
SERVER_IP = "127.0.0.1"

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) 
while True:
    msg = input("what to U want to send to the server ")
    sock.sendto(msg.encode() , (SERVER_IP , SERVER_PORT)) 
    response , remoteAdress = sock.recvfrom(1024)
    data = response.decode()
    if (data == "exit"):
        print("user chose to exit the program")
        break
    print (f" server sent: {data}")
sock.close()
