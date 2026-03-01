users = {"yosi" : {"password" : "Yos123" , "score" : 20 , "questions_asked" : [2,5]} , "roee" : {"password" : "r" , "score" : 25 , "questions_asked" : [2,5]}} # dictionary with key as the user name and value as password , score, and questions
logged_users= {"asdasd" : "yosi" , "1234fsas" : "roee"}
string = "table score:\n"
lowScoreUser = list(users.keys())[0]

if (len(users) == 0):
    print("there are not users")
arr=[]
for userName in users:
    arr.append(userName)
for i in range(0 , len(users)):
    lowScoreUser = arr[i]
    index = i
    for g in range(i + 1 , len(users)):
        if users.get(arr[g]).get("score") < users.get(lowScoreUser).get("score"):
            lowScoreUser = arr[g]
            index = g
    arr[i] , arr[index] = arr[index] , arr[i]
arr.reverse()
for i in range(0 , len(arr)):
    string += f"{i+1}. place: {arr[i]} with a score of {users.get(arr[i]).get("score")}\n"


string = "connected clients:\n"
for i in range(0 , len(logged_users) - 1):
    string += f"{list(logged_users.values())[i]} , "
string += list(logged_users.values())[len(logged_users) - 1]

import random
a = {"asd" : "a" , "asd" : "a" ,  "asd" : "a", "asd" : "a" , "asd" : "a"}


print (a)