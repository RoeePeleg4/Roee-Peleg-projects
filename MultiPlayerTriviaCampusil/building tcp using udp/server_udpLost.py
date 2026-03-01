import socket, random ,time
IP = "0.0.0.0"
PORT = 8821 
arrOfserialNums = []
TIMEOUT_IN_SECONDS = 10

# add packet id to send to client also


def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    print (fail)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops: server")

#getting protocol and returning its msg and serial number
def splitProtocol(protocol):
    isSeparated = 0
    msg = ""
    serialNumber = ""
    for i in range (0 , len(protocol)):
        if (protocol[i] == "|"):
            isSeparated +=1
            msg = protocol[0:i]
            serialNumber = protocol[i+1:len(protocol)]
    if isSeparated!=1:
        print ("WRONG PROTOCOL")
        return None , None
    return msg , serialNumber

sock = socket.socket(socket.AF_INET , socket.SOCK_DGRAM) 
print ("Server is running")
sock.bind((IP , PORT))

# trying to see if there is info, if there isnt send another request to the server
def recvfromClient(s , response, client_address):
    #if still trying recvfrom for 10 sec stop
    s.settimeout(TIMEOUT_IN_SECONDS) #idk w it is not in yellow
    try:
        responseFromClient , remoteAdress = s.recvfrom(1024)
        special_sendto(s , response , client_address)
    except:
        responseFromClient = None
        remoteAdress = None
    return responseFromClient , remoteAdress

while True:
    client_message , client_address = sock.recvfrom(1024)
    protocol = client_message.decode()
    msg , serialNumber = splitProtocol(protocol)
    #if didn't reach to server add it to a list of serial number the made it (if want to do a change in something do it inside the if so u dont do it twice)
    if (arrOfserialNums.count(serialNumber) == 0):
        arrOfserialNums.append(serialNumber)
        #add change here (so it wont be twice)
    print(arrOfserialNums)
    print (f"client send: {msg}")
    if (msg.lower() == "exit"):
        response = "exit"
        special_sendto(sock , response , client_address)
        # check for income requests
        responseFromClient = 'x'
        remoteAdress = '0.0.0.0'
        while (responseFromClient!=None and remoteAdress!=None):
            responseFromClient , remoteAdress = recvfromClient(sock , response , client_address)
        break 
    response = "hello " + msg
    special_sendto(sock , response , client_address)
print("User chose to exit the program")
sock.close()