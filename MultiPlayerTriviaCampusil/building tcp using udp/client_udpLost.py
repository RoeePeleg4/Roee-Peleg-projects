import socket , random
SERVER_PORT = 8821
SERVER_IP = "127.0.0.1"
SERIAL_NUMBER_FIELD_SIZE = 4
MAX_SERIAL_NUM = 10000
SERIAL_NUMBER = 0
TIMEOUT_IN_SECONDS = 5

def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    print (fail)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops: client")


#defines a serial Number
def defineSerialNumber(serialNumber):
    length = len(str(serialNumber))
    if (serialNumber == MAX_SERIAL_NUM):
        return ("0000")
    return ((SERIAL_NUMBER_FIELD_SIZE - length) * "0" + str(serialNumber))

#creating a protocol
def createProtocol(msg , serialNumber):
    return (msg + "|" + defineSerialNumber(serialNumber))




def recvfromServer(s , protocol):
    special_sendto(s, protocol , (SERVER_IP , SERVER_PORT)) 
    #if still trying recvfrom for 5 sec stop
    try:
        response , remoteAdress = sock.recvfrom(1024)
    except:
        print("a packet fell")
        response = None
        remoteAdress = None
    return response , remoteAdress




sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) 
#Time Out Set
sock.settimeout(TIMEOUT_IN_SECONDS)
while True:
    currentSerialNumber = defineSerialNumber(SERIAL_NUMBER)
    msg = input("what to U want to send to the server ")
    protocol = createProtocol(msg , currentSerialNumber)
    print (protocol)
    response = None
    remoteAdress = None
    while (response == None and remoteAdress == None):
        response , remoteAdress = recvfromServer(sock , protocol)
    data = response.decode()
    if (data == "exit"):
        print("user chose to exit the program")
        break
    print (f" server sent: {data}")
    SERIAL_NUMBER+=1
sock.close()
