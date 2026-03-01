import socket, chatlib
LOCAL_IP = "127.0.0.1"
SERVER_PORT = 8820
MAX_DATA_LENGTH = 1024

#page 3
# play a question with the server, didn't add yet up the score
def play_question(sock):
    msg_code , msg = build_send_recv_parse(sock , "GET_QUESTION")
    if (msg_code == "NO_QUESTIONS"):
        print("Out of questions GameOver")
        return
    arr = chatlib.split_data(msg, 5)
    if (arr == [None]):
        error_and_exit("Split the data coulden't occure well")
    answer = str(input(f"Question: {arr[1]}\n 1. {arr[2]}\n 2. {arr[3]}\n 3. {arr[4]}\n 4. {arr[5]}\nenter your answer: "))
    while answer!="1" and answer!="2" and answer!="3" and answer!="4":
        answer = str(input("please enter a valid answer: "))
    answerForQuestion = chatlib.join_data([arr[0] , str(answer)])
    print(answerForQuestion)
    cmd , data = build_send_recv_parse(sock , "SEND_ANSWER" , answerForQuestion)
    if (cmd == "CORRECT_ANSWER"):
        print(f"You were right the answer is: {answer}")
    else:
        print(f"You were wrong the answer is: {data}")

def get_logged_users(sock):
    cmd , users = build_send_recv_parse(sock , "LOGGED")
    print(f"the users that are now playing are {users}")


#page 2
# send a message to the server and recive and return it in a format of (cmd(msg_code) , data(msg))(might not be the right one)
def build_send_recv_parse (sock , cmd , data=""):
    build_and_send_message(sock , cmd , data)
    return recv_message_and_parse (sock)

#print user's score
def getScore(sock):
    #msg_coded , msg = build_send_recv_parse(sock , "MY_SCORE")
    msg_code , msg = build_send_recv_parse(sock , "MY_SCORE")
    #add exeption, I don't understand y needed
    print (f"Your current score is: {msg} points")

#print HighScoreTable
def get_highscore(sock):
    #msg_coded , msg = build_send_recv_parse(sock , "HIGHSCORE")
    msg_code , msg = build_send_recv_parse(sock , "HIGHSCORE")
    print(msg)




#functions that hasn't been checked (page 1)
#function that sends login request to the server until user connected
def login(sock):
    loginSucceeded = False
    while not loginSucceeded:
        #asks the user for details about itSelf
        userName = input("Enter your UserName: ")
        passWord = input("Enter Your PassWord: ")
        
        data = chatlib.join_data([userName , passWord])
        build_and_send_message(sock , "LOGIN" , data)
        msg_code , msg = recv_message_and_parse(sock)
        #msg_code , msg = chatlib.parse_message(msg)
        if (msg_code == "LOGIN_OK"):
            loginSucceeded = True
            print("You are logged in to the server")
        else:
            print("invalid user or password, try again")

#logging out the user from the server
def logout(sock):
    build_and_send_message(sock , "LOGOUT")
    protocol = sock.recv(MAX_DATA_LENGTH).decode()
    cmd , data = chatlib.parse_message(protocol)
    if cmd == "LOGOUT_CLIENT":
        return True
    return False


#return a socket that connects to the server
def connect():
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.connect((LOCAL_IP , SERVER_PORT))
    return sock

#print error message and quit
def error_and_exit(error_msg): #maybe need a change
    print(f"an ERROR has occured {error_msg}")
    exit()

#reciving data from the server and return (cmd(msg_code), data(msg))
def recv_message_and_parse(sock):
    data = sock.recv(1024).decode()
    return chatlib.parse_message(data)

#sends to an open socket a protocol in the right format
def build_and_send_message (sock , cmd , data = ""):
    sendToServer = chatlib.build_message(cmd , data)
    if sendToServer==None:
        #print Error message 
        return 
    print (f"the data that has been sent to the server {sendToServer}")
    #checking for invalid input by the user
    for i in range (len(data)):
        if (i == '#' or i == '|'):
            data[i] = " "
    sock.send(sendToServer.encode())

def main():
    sock = connect()
    login(sock)
    isLoggedOut = False
    while not isLoggedOut:
        choice = str(input ("Choose an opption:\nto logout press 1\nto see your score press 2\nto see High scores press 3\nto play a question press 4\nto get all active users press 5\nenter your choice: "))
        if (choice == "1"):
            isLoggedOut = logout(sock)
            #it closes the socket
        elif (choice == "2"):
            getScore(sock)
        elif (choice == "3"):
            get_highscore(sock)
        elif (choice == "4"):
            play_question(sock)
        elif (choice == "5"):
            get_logged_users(sock)
        else:
            print("invalid choice")
    sock.close()

if __name__ == '__main__':
    main()