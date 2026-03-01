import socket

sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
sock.connect(("127.0.0.1" , 8820))

while True:
    msg = input("enter your message ")
    sock.send(msg.encode())
    data = sock.recv(1024).decode()
    if (data == "Bye"):
        print ("Bye Bye")
        break
    else:
        print(f"this is the servers retrun: {data}")
sock.close()