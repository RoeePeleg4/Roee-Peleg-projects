import socket, random, time

sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
sock.bind(("0.0.0.0" , 8820))
sock.listen()
print("running")
socket_client , adress_client = sock.accept()
while True:
    data = socket_client.recv(1024).decode().lower()
    if (data == "quit"):
        socket_client.send("Bye".encode())
        break
    elif (data == "random"):
        data = str(random.randint(0,10))
    elif (data == "time"):
        data = time.ctime()
    elif (data == "name"):
        data = "practice_server25"
    else:
        data = "invalid command use the following: NAME, TIME, RANDOM, QUIT"
    socket_client.send(data.encode())
socket_client.close()
sock.close()