import pygame

#prams
# array of pawns
arr_char = []
#the size of the boar
BOARD_SIZE = (1000, 1000)
BOARD_SIDE = BOARD_SIZE[0] 
#size of the entire window
WINDOW_SIZE = (1400, 1000)
#pawns (soldigers size)
CHAR_SIDE = (BOARD_SIZE[1] / 8) * 0.8
CHAR_SIZE = (CHAR_SIDE , CHAR_SIDE)
#board depth into the window
DEPTH_X = (WINDOW_SIZE[0] - BOARD_SIZE[0]) / 2
DEPTH_Y = (WINDOW_SIZE[1] - BOARD_SIZE[1]) / 2
#is mouse pressed 
MOUSE_PRESSED = False
#which color turn is
TURN = "white"
#options of places to go
OPTIONS = []
#options to eat
OPTIONS_EAT = []
#define the color to move
COLOR_MOVE = (124,146,255)
#define the color to eat
COLOR_EAT = (255,115,115)
#defining if there is check
IS_CHECK = False

#on the display
#define screen
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Pygame Window")

# create a surface object, image is drawn on it.
board = pygame.image.load("pictures/board.png").convert()

# Scale the image to your needed size
board = pygame.transform.scale(board, BOARD_SIZE)

#update the board by characters position
def update(board , window , arr_char , board_size , depth_x , depth_y):
    cords_board = depth_x , depth_y
    window.blit(board, cords_board)
    for i in range(len(arr_char)):
        #if character was eaten
        if (arr_char[i].getX() == None and arr_char[i].getY()  == None):
            continue
        x , y = arr_char[i].getCordsForPlacemant(board_size[1] , CHAR_SIDE , depth_x , depth_y)
        char = pygame.image.load(f"pictures/{arr_char[i].getColor()}_{arr_char[i].getType()}.png").convert()
        char = pygame.transform.scale(char , CHAR_SIZE)
        window.blit(char, (x,y))

#retrun the middle cordinates in a format of (x,y) but (0,0) is in 8a, of any given cordinates
def getMiddleCords(board_side , x , y , depth_x , depth_y):
    sqr_side = (board_side / 8)
    x = x * sqr_side + sqr_side / 2 + depth_x
    y = y * sqr_side + sqr_side / 2 + depth_y
    return (x,y)

#class of the pawns and sold
#pos X , Y represent place on the board where (a,1) is (0,0)
class Character:
    def __init__(self, type , color , initial_pos):
        self.char_x = initial_pos[0]
        self.char_y = initial_pos[1]
        self.type = type
        self.color = color
        self.initial_pos = initial_pos
        self.isClicked = False
        self.arr_move_options = []
    def getArrMoveOptions(self):
        return self.arr_move_options
    def setArrMoveOptions(self , arr):
        self.arr_move_options = arr
    def getInitialPos(self):
        return self.initial_pos
    def getType(self):
        return self.type
    def getColor(self):
        return self.color
    def getX(self):
        return self.char_x
    def getY(self):
        return self.char_y
    def setX(self , x):
        self.char_x = x
    def setY(self , y):
        self.char_y = y
    def getIsClicked(self):
        return self.isClicked
    def setIsClicked(self):
        if (self.isClicked):
            self.isClicked = False
            return
        self.isClicked = True
    
    
    #return the cordinates that are required to place the image
    def getCordsForPlacemant(self, board_side , char_side , depth_x , depth_y):
        middle_x , middle_y = getMiddleCords(board_side , self.char_x , self.char_y , depth_x , depth_y)
        return (middle_x - (char_side / 2) , middle_y - (char_side / 2))

#updating the options to eat of each character in the color that gotten As argument
def updateOptionsEat(arr_char , king):
    for i in range(len(arr_char)):
        arr_char[i].setArrMoveOptions(getPlaces(arr_char[i] , arr_char , king)[1] + getPlaces(arr_char[i] , arr_char , king)[0])

#creation of the objects, and put them in an array
def creation():
    for i in range(8):
        #count is from 0,0 like maarach du meimadi
        white_pawn = Character("pawn", "white" , (i , 6))
        black_pawn = Character("pawn", "black" , (i , 1))
        arr_char.append(white_pawn)
        arr_char.append(black_pawn)
    white_bishop1 = Character ("bishop", "white" , (2, 7))
    white_bishop2 = Character ("bishop", "white", (5, 7))
    black_bishop1 = Character ("bishop", "black" , (2, 0))
    black_bishop2 = Character ("bishop", "black" , (5, 0))
    arr_char.append(white_bishop2)
    arr_char.append(white_bishop1)
    arr_char.append(black_bishop1)
    arr_char.append(black_bishop2)
    white_rook1 = Character("rook" , "white" , (0 , 7))
    white_rook2 = Character("rook" , "white" , (7 , 7))
    black_rook1 = Character("rook" , "black" , (0 , 0))
    black_rook2 = Character("rook" , "black" , (7 , 0))
    arr_char.append(white_rook1)
    arr_char.append(white_rook2)
    arr_char.append(black_rook1)
    arr_char.append(black_rook2)
    white_night1 = Character("knight" , "white" , (1 , 7))
    white_night2 = Character("knight" , "white" , (6 , 7))
    black_night1 = Character("knight" , "black" , (1 , 0))
    black_night2 = Character("knight" , "black" , (6 , 0))
    arr_char.append(white_night1)
    arr_char.append(white_night2)
    arr_char.append(black_night1)
    arr_char.append(black_night2)
    white_queen = Character("queen" , "white" , (4 , 4))
    black_queen = Character("queen" , "black" , (3 , 0))
    arr_char.append(white_queen)
    arr_char.append(black_queen)
    white_king = Character("king" , "white" , (4 , 7))
    black_king = Character("king" , "black" , (4 , 0))
    arr_char.append(white_king)
    arr_char.append(black_king)

#return the cube of the mouse in a format of (x,y)
def mouse_sqr(depth_x , depth_y , board_side):
    mouse_x , mouse_y = pygame.mouse.get_pos()
    y = ((mouse_y - depth_y) - ((mouse_y - depth_y) % (board_side / 8))) / (board_side / 8)
    x = ((mouse_x - depth_x) - ((mouse_x - depth_x) % (board_side / 8))) / (board_side / 8)
    return (x,y)

#return the object piece that the mouse is on, if it is not in position return None
def getPieceByPlace(turn , depth_x , depth_y , board_side):
    mouse_x , mouse_y = mouse_sqr(depth_x , depth_y , board_side)
    for i in range(len(arr_char)):
        if arr_char[i].getX() == mouse_x and arr_char[i].getY() == mouse_y:
            return arr_char[i]
    return None

#click listenter, check if left click is pressed
def check_pressed_mouse(isMousePressed):
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0] and not isMousePressed:
        return "pressed"
    elif mouse_pressed[0] and isMousePressed:
        return "pressed still"
    else:
        return "not pressed"

#return true if location open else return false
def isLocationOpen(cords, arr_char):
    for i in range(len(arr_char)):
        if (arr_char[i].getX() == cords[0] and arr_char[i].getY() == cords[1]):
            return False
    return True

#return true if cordinates are on the board and else if not
def isCordianteOnBoard(cordinate):
    return (cordinate[0]) >= 0 and (cordinate[0]) <=7 and (cordinate[1]) >= 0 and (cordinate[1]) <= 7

"""#return array of potential cordinates get x and y of the piece also
def potentialCords(cords , x , y):
    arr = []
    i = 1
    while isLocationOpen(cords , arr_char) and isCordianteOnBoard(cords):
        arr.append(cords)
        i+=1
    arr.append(cords)
    return arr"""

#return array of places where bishop can go
def bishop_move(piece):
    arr = []
    i = 1
    x = piece.getX()
    y = piece.getY()
    """arr += potentialCords((x + i,y + i) , x , y)
    arr += potentialCords((x - i,y - i))
    arr += potentialCords((x - i,y + i))
    arr += potentialCords((x + i,y - i))"""
    while isLocationOpen((x + i,y + i) , arr_char) and isCordianteOnBoard((x + i,y + i)):
        arr.append((x + i,y + i))
        i+=1
    arr.append((x + i,y + i))
    i = 1
    while isLocationOpen((x - i,y - i) , arr_char) and isCordianteOnBoard((x - i,y - i)):
        arr.append((x - i,y - i))
        i+=1
    arr.append((x - i,y - i))
    i = 1
    while isLocationOpen((x + i,y - i) , arr_char) and isCordianteOnBoard((x + i,y - i)):
        arr.append((x + i,y - i))
        i+=1
    arr.append((x + i,y - i))
    i = 1
    while isLocationOpen((x - i,y + i) , arr_char) and isCordianteOnBoard((x - i,y + i)):
        arr.append((x - i,y + i))
        i+=1
    arr.append((x - i,y + i))
    return arr

#return array of places where pawn can go
def pawn_move(piece):
    arr = []
    if piece.getColor() == "white":
        if not isLocationOpen((piece.getX() + 1 , piece.getY() - 1) , arr_char) and getPieceByLocation((piece.getX() + 1 , piece.getY() - 1) , arr_char)!=None and getPieceByLocation((piece.getX() + 1 , piece.getY() - 1) , arr_char).getColor()!=piece.getColor():
            arr.append((piece.getX() + 1 , piece.getY() - 1))
        if not isLocationOpen((piece.getX() - 1 , piece.getY() - 1) , arr_char) and getPieceByLocation((piece.getX() - 1 , piece.getY() - 1) , arr_char)!=None and getPieceByLocation((piece.getX() - 1 , piece.getY() - 1) , arr_char).getColor()!=piece.getColor():
            arr.append((piece.getX() - 1 , piece.getY() - 1))
        if isLocationOpen((piece.getX() , piece.getY() - 1) , arr_char):
            arr.append((piece.getX() , piece.getY() - 1))
            if piece.getInitialPos()[0] == piece.getX() and piece.getInitialPos()[1] == piece.getY() and isLocationOpen((piece.getX() , piece.getY() - 2) , arr_char):
                arr.append((piece.getX() , piece.getY() - 2))
    else:
        if not isLocationOpen((piece.getX() + 1 , piece.getY() + 1) , arr_char) and getPieceByLocation((piece.getX() + 1 , piece.getY() + 1) , arr_char)!=None and getPieceByLocation((piece.getX() + 1 , piece.getY() + 1) , arr_char).getColor()!=piece.getColor():
            arr.append((piece.getX() + 1 , piece.getY() + 1))
        if not isLocationOpen((piece.getX() - 1 , piece.getY() + 1) , arr_char) and getPieceByLocation((piece.getX() - 1 , piece.getY() + 1) , arr_char)!=None and getPieceByLocation((piece.getX() - 1 , piece.getY() + 1) , arr_char).getColor()!=piece.getColor():
            arr.append((piece.getX() - 1 , piece.getY() + 1))
        if isLocationOpen((piece.getX() , piece.getY() + 1) , arr_char):
            arr.append((piece.getX() , piece.getY() + 1))
            if piece.getInitialPos()[0] == piece.getX() and piece.getInitialPos()[1] == piece.getY() and isLocationOpen((piece.getX() , piece.getY() + 2) , arr_char):
                arr.append((piece.getX() , piece.getY() + 2))
    return arr

#return array of places where rook can go
def rook_move(piece):
    arr = []
    i = 1
    x = piece.getX()
    y = piece.getY()
    while isLocationOpen((x + i,y) , arr_char) and isCordianteOnBoard((x + i,y)):
        arr.append((x + i,y))
        i+=1
    arr.append((x + i,y))
    i = 1
    while isLocationOpen((x - i,y) , arr_char) and isCordianteOnBoard((x - i,y)):
        arr.append((x - i,y))
        i+=1
    arr.append((x - i,y))
    i = 1
    while isLocationOpen((x,y + i) , arr_char) and isCordianteOnBoard((x,y + i)):
        arr.append((x,y + i))
        i+=1
    arr.append((x,y + i))
    i = 1
    while isLocationOpen((x,y - i) , arr_char) and isCordianteOnBoard((x,y - i)):
        arr.append((x,y - i))
        i+=1
    arr.append((x,y - i))
    return arr

#return array of places where king can go
def king_move(piece):
    arr = []
    x = piece.getX()
    y = piece.getY()
    arr.append((x ,y + 1))
    arr.append((x ,y - 1))
    arr.append((x + 1,y))
    arr.append((x - 1 ,y))
    arr.append((x + 1 ,y + 1))
    arr.append((x - 1 ,y + 1))
    arr.append((x + 1 ,y - 1))
    arr.append((x - 1 ,y - 1))
    return arr

#return array of places where knight can go
def knight_move(piece):
    arr = []
    x = piece.getX()
    y = piece.getY()
    arr.append((x + 1 , y + 2))
    arr.append((x - 1 , y + 2))
    arr.append((x + 1 , y - 2))
    arr.append((x - 1 , y - 2))
    arr.append((x + 2 , y + 1))
    arr.append((x + 2 , y - 1))
    arr.append((x - 2 , y - 1))
    arr.append((x - 2 , y + 1))
    return arr

#get cordinates as argument and returns the piece object, else return None
def getPieceByLocation(cords , arr_char):
    for i in range(len(arr_char)):
        if (arr_char[i].getX() == cords[0] and arr_char[i].getY() == cords[1]):
            return arr_char[i]
    return None


#returns array of the places (x,y) that the piece can go
def getPlaces(piece , arr_char , king):
    eatable_arr = []
    options_arr = []
    #potential
    arr_potential = []
    #for the pieces that had been eaten
    if piece.getX() == None and piece.getY() == None:
        pass
    elif piece.getType()=="pawn":
        arr_potential = pawn_move(piece)
    elif piece.getType()=="bishop":
        arr_potential = bishop_move(piece)
    elif piece.getType()=="rook":
        arr_potential = rook_move(piece)
    elif piece.getType()=="knight":
        arr_potential = knight_move(piece)
    elif piece.getType()=="queen":
        #queen is a combination of rook and bishop so wiil use both
        arr_potential = bishop_move(piece)
        arr_potential += rook_move(piece)
    #else is king
    else:
        arr_potential = king_move(piece)
    for i in range (len(arr_potential)):
        if isLocationOpen(arr_potential[i] , arr_char) and arr_potential[i][0] >= 0 and arr_potential[i][0] <=7 and arr_potential[i][1] >= 0 and arr_potential[i][1] <=7:
            options_arr.append(arr_potential[i])
        elif not isLocationOpen(arr_potential[i] , arr_char) and getPieceByLocation(arr_potential[i] , arr_char).getColor() != piece.getColor():
            eatable_arr.append(arr_potential[i])
    """if (piece.getColor() == "black" and piece.getType() == "queen"):
        print (eatable_arr)"""
    return options_arr , eatable_arr

#get piece index by location
def getPieceIndexByLocation(arr_char , piece):
    for i in range(len(arr_char)):
        if arr_char[i] is piece:
            return i
    return None
#return true if it can move to that location without a check else false
def canMove(piece , arr_char , position , king_by_piece_color):
    piece_original_location = (piece.getX() , piece.getY())
    index = getPieceIndexByLocation(arr_char , piece)
    if index == None:
        print("Index is None")
    arr_char[index].setX(position[0])
    arr_char[index].setY(position[1])
    index_of_none = -1
    for i in range(len(arr_char)):
        if arr_char[i].getX() == arr_char[index].getX() and arr_char[i].getY() == arr_char[index].getY() and arr_char[index] is not arr_char[i]:
            saveLocation = (arr_char[i].getX() , arr_char[i].getY())
            print(arr_char[i].getX() , arr_char[i].getY(),  "roee")
            arr_char[i].setX(None)
            arr_char[i].setY(None)
            index_of_none = i
            break
    updateOptionsEat(arr_char , king_by_piece_color)
    print(piece.getColor() , piece.getType())
    for i in range(len(arr_char)):
        if piece.getColor() != arr_char[i].getColor():
            if (king_by_piece_color.getX() , king_by_piece_color.getY()) in arr_char[i].getArrMoveOptions():
                print("hellooooo")
                arr_char[index].setX(piece_original_location[0])
                arr_char[index].setY(piece_original_location[1])
                if index_of_none != -1:
                    arr_char[index_of_none].setX(saveLocation[0])
                    arr_char[index_of_none].setY(saveLocation[1])
                updateOptionsEat(arr_char , king_by_piece_color)
                return False
    arr_char[index].setX(piece_original_location[0])
    arr_char[index].setY(piece_original_location[1])
    if index_of_none != -1:
        arr_char[index_of_none].setX(saveLocation[0])
        arr_char[index_of_none].setY(saveLocation[1])
    updateOptionsEat(arr_char , king_by_piece_color)
    return True

    
#if there is an already clicked piece it cancels it
def already_clicked(arr_char):
    for i in range(len(arr_char)):
        if (arr_char[i].getIsClicked() == True):
            arr_char[i].setIsClicked()
            return
        
#draw the options of the player
def drawOptions(options_arr , depth_x , depth_y , color):
    for i in range(len(options_arr)):
        circle_x , circle_y = getMiddleCords(BOARD_SIDE , options_arr[i][0] , options_arr[i][1] , depth_x , depth_y)
        pygame.draw.circle(window , color , (circle_x , circle_y) , 10)

#switching turns
def switchTurn(turn):
    if turn == "white":
        print("Switching turn yo black")
        return "black"
    else:
        print("Switching turn yo white")
        return "white"

#getting a list of cordinates and checking if a king is one of them , and getting the oppsite color of the TURN as prameter, return true if the king is in the list of positions and elese false
def isCheck(arr_char , opp_turn , turn):
    opp_king = None
    for i in range(len(arr_char)):
        if arr_char[i].getType() == "king" and arr_char[i].getColor() == opp_turn:
            opp_king = arr_char[i]
            break
    king_pos = (opp_king.getX() , opp_king.getY())
    for i in range(len(arr_char)):
        if turn == arr_char[i].getColor():
            if (king_pos in arr_char[i].getArrMoveOptions()):
                return True
    return False

#return the oposite color
def getOppositeColor(color):
    if color!="black" and color!="white":
        return None
    elif color=="black":
        return "white"
    return "black"

#return the positions that the king in the opossite color can move, return's his moving places, else return None
def canKingMoveFunc(opp_color , arr_char):
    for i in range(len(arr_char)):
        if arr_char[i].getType() == "king" and opp_color == arr_char[i].getColor():
            moving_opttions , eating_options = getPlaces(arr_char[i] , arr_char)
            arr = moving_opttions + eating_options
            arr.append((arr_char[i].getX() , arr_char[i].getY()))
            return arr
    return None

#returning the positions that the king is allowed to move
def canPieceBeEaten(arr_char , arr_positions_piece , opp_color):
    # array of the pieces that can eat the piece that we want to check if can move
    arr_valid_positions = []
    for i in range(len(arr_positions_piece)):
        for g in range(len(arr_char)):
            if (not (arr_char[g].getColor() == opp_color and arr_positions_piece[i] in arr_char[g].getArrMoveOptions())):
                arr_valid_positions.append(arr_positions_piece[i])
    return arr_valid_positions

#checking objects can move and get the king out of danger, else if there are no objects like that return empty list
"""def getBlocking(arr_dangering , moving_positions):
    arr_all_moving_options = []
    for i in range(len(moving_positions)):
        for g in range(len(arr_dangering)):
            if moving_positions[i] in arr_dangering[g].getArrMoveOptions() and arr_dangering[g].getType() is not "knight":
                arr_all_moving_options.append([arr_dangering[g] , moving_positions[i]])
    return arr_all_moving_options"""

#getting the objects that can deffend the king, as args get the dangering piece and it's poitions , dictionary
#the color is the color of the king
#return a dictionary that contains {object : [potential moving positions]}
def deffendObjects(king , color_king, arr_char):
    #for the return a dict that contains, object : [list of the places it can go to deffend the king]
    dict_object_deffenders = {}
    #checking which of the opposite colors can eat the king in current position
    dangering_objects = []
    for i in range(len(arr_char)):
        if (arr_char[i].getColor() != color_king and (king.getX() , king.getY()) in arr_char[i].getArrMoveOptions()):
            dangering_objects.append(arr_char[i])
    for i in range(len(dangering_objects)):
        for g in range(len(arr_char)):
            if (arr_char[g].getColor() == color_king):
                #check if the piece from the king side has the same options to go as the dangering piece
                for h in range(len(arr_char[g].getArrMoveOptions())):
                    arr = dangering_objects[i].getArrMoveOptions()
                    arr.append((dangering_objects[i].getX() , dangering_objects[i].getY()))
                    if arr_char[g].getType() == "knight":
                        if arr_char[g].getArrMoveOptions()[h] == (dangering_objects[i].getX() , dangering_objects[i].getY()):
                            if (arr_char[g] in list(dict_object_deffenders.keys())):
                                dict_object_deffenders[arr_char[g]].append(arr_char[g].getArrMoveOptions()[h])
                            else:
                                dict_object_deffenders.update({arr_char[g] : arr_char[g].getArrMoveOptions()[h]})
                    elif arr_char[g].getArrMoveOptions()[h] in arr:
                        #add the value to the list
                        if (arr_char[g] in list(dict_object_deffenders.keys())):
                            dict_object_deffenders[arr_char[g]].append(arr_char[g].getArrMoveOptions()[h])
                        else:
                            dict_object_deffenders.update({arr_char[g] : arr_char[g].getArrMoveOptions()[h]})
    return dict_object_deffenders
    

#returning the valid places that the king can go
def getValidKingPositions(dict_dangering , moving_positions):
    list_dangering = list(dict_dangering.keys())
    valid_moving = []
    for i in range(len(moving_positions)):
        if moving_positions[i] not in list_dangering:
            valid_moving.append(moving_positions[i])
    return valid_moving

#returning the king by color
def getKing(color , arr_char):
    for i in range(len(arr_char)):
        if (arr_char[i].getColor() == color and arr_char[i].getType() == "king"):
            return arr_char[i]
    return None
def main():
    #creation of objects
    creation()
    #update the screen with the values every few frames
    update(board, window, arr_char, BOARD_SIZE , DEPTH_X , DEPTH_Y)
    #what happens on screen
    #set the current working piece
    currentPiece = None 
    
    #set the loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #checking if the mouse is pressed only once on each piece
        # and set if the object is clicked
        #only one can be clicked at a time
        global MOUSE_PRESSED , TURN , OPTIONS_EAT
        #a boolean expression that tells if I should update in ui
        should_update = False
        is_moved = False
        #checking if there is check
        king_turn = getKing(TURN, arr_char)
        opp_color = getOppositeColor(TURN)
        updateOptionsEat(arr_char , king_turn)
        """IS_CHECK = (opp_color != None and isCheck(arr_char , opp_color , TURN))
        if (IS_CHECK):
            print("check")
        # checking check mate, check mate is happening in the victim's turn
        if(IS_CHECK):
            king = getKing(TURN , arr_char)
            if king == None:
                print("[SYSTEM] an error has ocurred")
                return
            canKingMove = False
            canBlock = False
            #checking if the king can move
            moving_positions = canKingMoveFunc(opp_color , arr_char)
            #in a format of position : dangering objects
            valid_places_to_go_king = canPieceBeEaten(arr_char , moving_positions , opp_color)
            #valid_places_to_go_king =getValidKingPositions(dict_dangering , moving_positions)
            #check the entire pieces options to move
            dict_moving_options = deffendObjects(king , TURN , arr_char)
            if len(valid_places_to_go_king) == 0:
                canKingMove = False
            else:
                canKingMove = True
                dict_moving_options.update({king : valid_places_to_go_king})
            if (not (len(dict_moving_options) == 1 and len(dict_moving_options[king]) == 0)):
                canBlock = True
            #check the king's options to move
            if (canKingMove == False and canBlock == False):
                print(f"game over, {TURN} wins!")"""
        #current piece is the one you see where it can move
        #piece is the one the current piece can eat
        if (check_pressed_mouse(MOUSE_PRESSED) == "pressed"):
            piece = getPieceByPlace(TURN , DEPTH_X , DEPTH_Y , BOARD_SIDE)
            #clicked on the piece with the same color as turn, and set that it got clicked and that this is the piece that the player wants to move
            if piece != None and TURN == piece.getColor():
                if piece.getIsClicked() == True:
                    piece.setIsClicked()
                    currentPiece = None
                    OPTIONS = []
                    should_update = True
                else:
                    currentPiece = piece
                    should_update = True
                    OPTIONS , OPTIONS_EAT = getPlaces(piece , arr_char , king_turn)
                    #counting the amount of items that got deleted
                    deleted_items = 0
                    if currentPiece.getType() == "pawn":
                        print("pawn")
                    delete_by_index = []
                    for i in range(len(OPTIONS)):
                        if not canMove(currentPiece , arr_char , OPTIONS[i] , king_turn):
                            delete_by_index.append(i)
                    print(delete_by_index)
                    for index in delete_by_index:
                        del OPTIONS[index - deleted_items]
                        deleted_items +=1
                    print("roee" , piece.getX() , piece.getY())
                    delete_by_index = []
                    #counting the amount of items that got deleted
                    deleted_items = 0
                    for g in range(len(OPTIONS_EAT)):
                        if OPTIONS_EAT[g][0] == 0 and OPTIONS_EAT[g][1] == 4:
                            pass
                        if not canMove(currentPiece , arr_char , OPTIONS_EAT[g] , king_turn):
                            delete_by_index.append(g)
                    for index in delete_by_index:
                        del OPTIONS_EAT[index - deleted_items]
                        deleted_items +=1
                    already_clicked(arr_char)
                    piece.setIsClicked()
            #clicked on the player and then on another player from opsing team
            elif currentPiece!=None and piece!=None and piece.getColor() != TURN and TURN == currentPiece.getColor():
                future_pos = mouse_sqr(DEPTH_X , DEPTH_Y , BOARD_SIDE)
                if (future_pos in OPTIONS_EAT):
                    eat_peace = getPieceByLocation(future_pos , arr_char)
                    eat_peace.setX(None)
                    eat_peace.setY(None)
                    print(f"future position {mouse_sqr(DEPTH_X , DEPTH_Y , BOARD_SIDE)}")
                    currentPiece.setY(future_pos[1])
                    currentPiece.setX(future_pos[0])
                    TURN = switchTurn(TURN)
                    should_update = True
                    is_moved = True
            #click on a character from his team and than on another spot on the board
            elif currentPiece!=None and piece == None:
                future_pos = mouse_sqr(DEPTH_X , DEPTH_Y , BOARD_SIDE)
                if (future_pos in OPTIONS):
                    currentPiece.setY(future_pos[1])
                    currentPiece.setX(future_pos[0])
                    TURN = switchTurn(TURN)
                    should_update = True
                    is_moved = True
            MOUSE_PRESSED = True
        elif (check_pressed_mouse(MOUSE_PRESSED) == "not pressed"):
            MOUSE_PRESSED = False
        
        
        #update the screen
        if should_update:
            update(board, window, arr_char, BOARD_SIZE , DEPTH_X , DEPTH_Y)
            if currentPiece is not None and currentPiece.getIsClicked() and not is_moved:
                print("in")
                drawOptions(OPTIONS , DEPTH_X , DEPTH_Y , COLOR_MOVE)
                drawOptions(OPTIONS_EAT , DEPTH_X , DEPTH_Y , COLOR_EAT)
        #clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()