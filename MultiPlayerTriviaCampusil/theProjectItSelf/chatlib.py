#values
CMD_FIELD_LENGTH = 16
LENGTH_FIELD_LENGTH = 4
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH - 1

#get data and then split it due to # and returns an array (opposite of, join_data)
def split_data (string , amount):
    startingIndex = 0
    charIndex = 0
    amountCounter = 0
    string = str(string)
    if (str(amount).isdigit() == False):
        return [None]
    arr = []
    for char in string:
        if char == '#':
            amountCounter +=1
            arr.append(string[startingIndex:charIndex])
            startingIndex = charIndex + 1
        charIndex+=1
    #for the last element
    arr.append(string[startingIndex:charIndex])
    if amountCounter==amount:
        return arr
    return [None]

#adding the datas from an array into data format (opposite of, split_data)
def join_data(arr):
    if (len(arr) == 0):
        return None
    stringToReturn = ""
    for i in range(0,len(arr) - 1):
        stringToReturn += str(arr[i]) + "#"
    #add last word
    stringToReturn += str(arr[len(arr) - 1])
    return (stringToReturn)

#building message in the protocol format
def build_message (type, data = ""):
    type = str(type)
    data = str(data)
    if len(type) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
        return None
    type = type.replace (" ","")
    type += " " * (CMD_FIELD_LENGTH - len(type))
    numberInBetween = len(data)
    strNum = "0" * (LENGTH_FIELD_LENGTH - len(str(numberInBetween))) + str(numberInBetween)
    return f"{type}|{strNum}|{data}"

# returns the Command and the data from a protocol (cmd(msg_code) , data(msg))
def parse_message (protocol):
    startingIndex = 0
    charIndex = 0
    counterOfLine = 0
    arr = []
    protocol = str(protocol)
    for char in protocol:
        if char == '|':
            counterOfLine+=1
            arr.append(protocol[startingIndex:charIndex])
            startingIndex = charIndex + 1
        charIndex+=1
    arr.append(protocol[startingIndex:charIndex])
    if (counterOfLine !=2 or len(arr[0])!=CMD_FIELD_LENGTH or len(arr[2]) > MAX_DATA_LENGTH or len(arr[1]) != LENGTH_FIELD_LENGTH):
        return (None, None)
    for i in range (0,len(arr[1])):
        if (char == " "):
            arr[1][i] = "0"
        if (arr[1][i].isdigit()==False and arr[1][i]!=" "):
            return (None, None)
    arr[0] = arr[0].replace(" ", "")
    return arr[0], arr[2]