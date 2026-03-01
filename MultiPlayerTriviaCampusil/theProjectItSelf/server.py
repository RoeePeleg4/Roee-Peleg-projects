import socket, chatlib, select , random

#all users
users = {"yosi" : {"password" : "Yos123" , "score" : 10 , "questions_asked" : []} , "roee" : {"password" : "r" , "score" : 25 , "questions_asked" : []} , "a" : {"password" : "a" , "score" : 10 , "questions_asked" : []}, "b" : {"password" : "b" , "score" : 5 , "questions_asked" : []}, "c" : {"password" : "c" , "score" : 50 , "questions_asked" : []}} # dictionary with key as the user name and value as password , score, and questions
#only the logged ones
logged_users = {} # in a format of {sokcet.getpeername() : username}
questions = {1 : {"question":"How much is 2+2" , "answers":["3","4","2","1"] , "correct":2}} # contain dictionary key : {q :_ , a:[] , c : _}
LISTEN_IP = "0.0.0.0"
SERVER_PORT = 8820
MAX_DATA_LENGTH = 1024
#messages to send in a queue
messages_to_send = [] # include tuples (sock , msg_to_send) the msg is unencoded

#I need to handle focible closing

#printing the ip and port of sockets in a tuple (ip , port)
def print_client_sockets(sockets):
    for s in sockets:
        print(s.getpeername())
#return score table to the client
def handle_highscore_message(sock):
    string = "table score:\n"
    lowScoreUser = list(users.keys())[0]
    if (len(users) == 0):
        build_and_send_message(sock , "ALL_SCORE" , string + "there are no users in the system\n")
    arr=[]
    for userName in list(users.keys()):
        arr.append(userName)
    for i in range(0 , len(users)):
        lowScoreUser = arr[i]
        index = i
        for g in range(i , len(users)):
            if users.get(arr[g]).get("score") < users.get(lowScoreUser).get("score"):
                lowScoreUser = arr[g]
                index = g
        value_to_save = arr[index] #the least amount
        arr[index] = arr[i]
        arr[i] = value_to_save
    arr.reverse() # because I've done from lowest to highest
    #arr = list(set(arr))
    for i in range(0 , len(arr)):
        string += f"{i+1}. place: {arr[i]} with a score of {users.get(arr[i]).get("score")}\n"
    build_and_send_message(sock , "ALL_SCORE" , string)
    
#genarating random question from the "data base" of questions
def create_random_question():
    rndNum = random.randint(0 , len(questions) - 1)
    key = list(questions.keys())[rndNum]
    protocol_data = f"{key}#{questions.get(key).get("question")}#{questions.get(key).get("answers")[0]}#{questions.get(key).get("answers")[1]}#{questions.get(key).get("answers")[2]}#{questions.get(key).get("answers")[3]}"
    return protocol_data

#send a random question to the client, if client finished all questions in will send an error message
def handle_question_message(sock):
    #print (logged_users)
    if (len(users.get(logged_users.get(sock.getpeername())).get("questions_asked")) == len(questions)):
        build_and_send_message(sock , "NO_QUESTIONS")
        return 
    if (len(questions) == 0):
        send_error(sock , "there are no questions in the data base")
        return
    isValidQuestion = False
    userName = logged_users.get(sock.getpeername())
    keyQ = None
    #infinite loop (unperpusley)
    while isValidQuestion == False:
        #asuming that create random doesNot genarate errors
        randomQ = create_random_question()
        #getting the key of the question
        for i in range(0 , len(randomQ)):
            if (randomQ[i] == "#"):
                keyQ = randomQ[0:i]
                break
        if not keyQ in users.get(userName).get("questions_asked"):
            isValidQuestion = True
    build_and_send_message(sock , "YOUR_QUESTION" , randomQ)

#get the answer from user and send to the uesr if it was right
def handle_answer_message(sock , userName , answer):
    arr = chatlib.split_data(answer , 1)
    print(arr[0])
    if (arr[0]==None):
        send_error(sock, "There has been an error with the send of your answer")
        return
    if (str(questions.get(int(arr[0])).get("correct")) == arr[1]):
        users[userName]["score"] +=5
        build_and_send_message(sock , "CORRECT_ANSWER")
    else:
        build_and_send_message(sock , "WRONG_ANSWER" , questions.get(int(arr[0])).get("correct"))
    users[userName]["questions_asked"].append(int(arr[0]))
    print(users[userName]["questions_asked"])

#return to the client all of the logged clients
def handle_logged_message(sock):
    string = ""
    arr_already_in = []
    if (len(logged_users)==0):
        build_and_send_message(sock , "LOGGED_ANSWER" , string + "there are no connected clients\n")
    for i in range(0 , len(logged_users) - 1):
        print (list(logged_users.values())[i] , arr_already_in)
        if not list(logged_users.values())[i] in arr_already_in:
            #string += f"{list(logged_users.values())[i]} , "
            arr_already_in.append(list(logged_users.values())[i])
    if not list(logged_users.values())[len(logged_users) - 1] in arr_already_in:
        #string += list(logged_users.values())[len(logged_users) - 1]
        arr_already_in.append(list(logged_users.values())[len(logged_users) - 1])
    for i in range(len(arr_already_in)):
        if (i == len(arr_already_in) - 1):
            string+=arr_already_in[i]
        else:
            string+=f"{arr_already_in[i]} , "
    build_and_send_message(sock , "LOGGED_ANSWER" , string)


#retrun the score to the client 
def handle_getscore_message(sock):
    if logged_users.get(sock.getpeername())==None:
        send_error("Invalid userName")
    userName = logged_users.get(sock.getpeername())
    score = users.get(userName).get("score")
    build_and_send_message(sock , "YOUR_SCORE" , str(score))

#reciving data from the server and return (cmd(msg_code), data(msg))
def recv_message_and_parse(sock):
    data = sock.recv(1024).decode()
    print (f"[CLIENT] {data}")
    return chatlib.parse_message(data)

#sends to an open socket a protocol in the right format
def build_and_send_message (sock , cmd , data = ""):
    sendToClient = chatlib.build_message(cmd , data)
    if sendToClient==None:
        #print Error message 
        return 
    print (f"[SERVER] {sendToClient}")
    messages_to_send.append((sock , sendToClient))
    #sock.send(sendToClient.encode())

#define server socket
def setup_socket():
    socket_server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    socket_server.bind((LISTEN_IP , SERVER_PORT))
    socket_server.listen()
    print("[SERVER] running")
    return socket_server

# send error message to the client
def send_error(sock , error_msg):
    build_and_send_message(sock , "ERROR" , "[SERVER] " + error_msg)

#confirm login or not and return userName
def handle_login_message(sock , data): #only data without command 
    arr = chatlib.split_data(data , 1)
    if (len(arr)!=2 or arr[0] == None or arr[1]==None):
        send_error(sock , "There is a problem with the data")
        return
    #if (arr[1] in list(logged_users.values())):
    #    send_error(sock , "same user is logged in another computer")
    #    return
    if (users.get(arr[0])!=None):
        if (users.get(arr[0]).get("password") == arr[1]):
            build_and_send_message(sock , "LOGIN_OK")
            logged_users.update({sock.getpeername() : arr[0]})
            print (logged_users)
            return arr[0]
        else:
            send_error(sock , "Password is incorrect")
    else:
        send_error(sock , "User was Not found")

#closing connection with the client socket
def handle_logout_message(sock):
    build_and_send_message(sock , "LOGOUT_CLIENT")

#handle ctl + c
def signal_handler(signal, frame , client_socket):
    return True

#directioning via command type, return True if it is a logout msg inFact
def handle_client_message(sock , cmd ,data):
    userName = logged_users.get(sock.getpeername())
    if (cmd == "LOGIN" and logged_users.get(sock.getpeername())==None):
        print("hello world!")
        handle_login_message(sock , data)
        return False
    elif(cmd == "LOGOUT" and logged_users.get(sock.getpeername())!=None):
        handle_logout_message(sock)
        return True
    elif (cmd == "MY_SCORE" and logged_users.get(sock.getpeername())!=None):
        handle_getscore_message(sock)
        return False
    elif (cmd == "HIGHSCORE" and logged_users.get(sock.getpeername())!=None):
        handle_highscore_message(sock)
        return False
    elif (cmd == "LOGGED" and logged_users.get(sock.getpeername())!=None):
        handle_logged_message(sock)
        return False
    elif (cmd == "GET_QUESTION" and logged_users.get(sock.getpeername())!=None):
        print("hi")
        handle_question_message(sock)
        return False
    elif (cmd == "SEND_ANSWER" and logged_users.get(sock.getpeername())!=None):
        handle_answer_message(sock , userName , data)
        return False
    else:
        send_error(sock, "Invalid command")
        return False

def main():
    #sig = signal.signal(signal.SIGINT, signal_handler)
    server_socket = setup_socket()
    client_sockets = []
    while True:
        ready_to_read , ready_to_write , in_error = select.select([server_socket] + client_sockets ,client_sockets , [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                client_socket , client_address = current_socket.accept()
                print(f"new client joined! with the address of {client_address}")
                client_sockets.append(client_socket)
                cmd , data = recv_message_and_parse(client_socket)
                handle_client_message(client_socket , cmd , data)
                #cmd , data = recv_message_and_parse(client_socket)
                #current_socket.send(data.encode())
            else:
                print ("new data from current client")
                try: 
                    cmd , data = recv_message_and_parse(current_socket)
                except:
                    handle_logout_message(current_socket)
                    print ("cmd window close and we closed connection with the client")
                print (cmd , data , "asd")
                if (handle_client_message(current_socket , cmd , data) == True): 
                    client_sockets.remove(current_socket)
                    logged_users.pop(current_socket.getpeername())
                    break
                # inorder to face forcing closing of by the client, didnt do it yet
                #if ((cmd == "" and data == "") or (cmd == None and data == None)):
                #    handle_logout_message(current_socket)
        for msg in messages_to_send:
            sock , data = msg
            print (data)
            if sock in ready_to_write:
                sock.send(data.encode())
                print (data + "roee")
                messages_to_send.remove(msg)
                cmd, msg = chatlib.parse_message(data)
                if (cmd == "LOGOUT_CLIENT"):
                    print (str(len(logged_users)) + " tomi")
                    sock.close()
                    print (str(len(logged_users)) + " roee")
        #current_socket.close()
            
    
        

        

if __name__ == '__main__':
    main()
    