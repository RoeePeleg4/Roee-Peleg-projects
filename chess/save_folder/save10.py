import pygame
from time import sleep

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

#for sound
#Instantiate mixer
pygame.mixer.init()

"""#load audio files
pygame.mixer.music.load('sounds/capture.wav')
pygame.mixer.music.load('sounds/move.wav')"""

#Set preferred volume
pygame.mixer.music.set_volume(0.2)

#on the display
#define screen
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("My Pygame Window")

# create a surface object, image is drawn on it.
board = pygame.image.load("pictures/board.png").convert()

# Scale the image to your needed size
board = pygame.transform.scale(board, BOARD_SIZE)

#update the board by characters position
def update(board , window , arr_char , board_size , depth_x , depth_y , currentPiece , is_moved , options , options_eat):
    cords_board = depth_x , depth_y
    window.blit(board, cords_board)
    if currentPiece is not None and is_moved is not None:
        if currentPiece is not None and currentPiece.getIsClicked() and not is_moved:
            drawMovingOptions(options , depth_x , depth_y , False)
            drawMovingOptions(options_eat , depth_x , depth_y , True)
    for i in range(len(arr_char)):
        #if character was eaten
        if (arr_char[i].getX() == None and arr_char[i].getY()  == None):
            continue
        x , y = arr_char[i].getCordsForPlacemant(board_size[1] , CHAR_SIDE , depth_x , depth_y)
        char = pygame.image.load(f"pictures/{arr_char[i].getColor()}_{arr_char[i].getType()}.png")
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
        self.isMoved = False
    def getIsMoved(self):
        return self.isMoved
    def setIsMoved(self , boolean):
        self.isMoved = boolean
    def getArrMoveOptions(self):
        return self.arr_move_options
    def setArrMoveOptions(self , arr):
        self.arr_move_options = []
        self.arr_move_options = arr
    def getInitialPos(self):
        return self.initial_pos
    def getType(self):
        return self.type
    def setType(self , type):
        self.type = type
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
        arr_char[i].setArrMoveOptions(getPlaces(arr_char[i] , arr_char)[1] + getPlaces(arr_char[i] , arr_char)[0])

#creation of the objects, and put them in an array
def creation():
    for i in range(8):
        #count is from 0,0 like maarach du meimadi
        white_pawn = Character("pawn", "white" , (i , 6))
        black_pawn = Character("pawn", "black" , (i , 1))
        arr_char.append(white_pawn)
        arr_char.append(black_pawn)
    white_bishop1 = Character ("bishop", "white" , (2,7)) 
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
    white_queen = Character("queen" , "white" , (3 , 7)) #(4,4)
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
def getPieceByPlace(depth_x , depth_y , board_side):
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

#return array of places where bishop can go
def bishop_move(piece):
    arr = []
    i = 1
    x = piece.getX()
    y = piece.getY()
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
def getPlaces(piece , arr_char):
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
            arr_char[i].setX(None)
            arr_char[i].setY(None)
            index_of_none = i
            break
    updateOptionsEat(arr_char , king_by_piece_color)
    for i in range(len(arr_char)):
        if piece.getColor() != arr_char[i].getColor():
            if (king_by_piece_color.getX() , king_by_piece_color.getY()) in arr_char[i].getArrMoveOptions():
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

#draw the players options to go
def drawMovingOptions(options_arr , depth_x , depth_y , isEat):
    for i in range(len(options_arr)):
        circle_x , circle_y = getMiddleCords(BOARD_SIDE , options_arr[i][0] , options_arr[i][1] , depth_x , depth_y)
        if (options_arr[i][0] + options_arr[i][1]) % 2 == 0:
            color = (202,203,178,255)
        else:
            color = (101,128,67,255)
        if isEat:
            pygame.draw.circle(window , color , (circle_x , circle_y) , 60 , 10)
        else:
            pygame.draw.circle(window , color , (circle_x , circle_y) , 15)

#switching turns
def switchTurn(turn):
    if turn == "white":
        print("Switching turn to black")
        return "black"
    else:
        print("Switching turn to white")
        return "white"

#getting a list of cordinates and checking if a king is one of them , and getting the oppsite color of the TURN as prameter, return true if the king is in the list of positions and elese false
def isCheck(arr_char , color):
    king = None
    for i in range(len(arr_char)):
        if arr_char[i].getType() == "king" and arr_char[i].getColor() == color:
            king = arr_char[i]
            break
    king_pos = (king.getX() , king.getY())
    for i in range(len(arr_char)):
        if arr_char[i].getColor()!=color:
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

#returning the king by color
def getKing(color , arr_char):
    for i in range(len(arr_char)):
        if (arr_char[i].getColor() == color and arr_char[i].getType() == "king"):
            return arr_char[i]
    return None

#update the moving options of each piece and deleting the places that he can't move
def updateMove(piece , king):
    #which means equals the color of the someone that his turn is is
    if (piece.getX() == None and piece.getY() == None) or piece.getColor()!=king.getColor():
        return None
    delete_by_index = []
    deleted_items = 0
    tmp_list = piece.getArrMoveOptions()
    for g in range(len(tmp_list)):
        if not canMove(piece , arr_char , tmp_list[g] , king):
            delete_by_index.append(g)
    for index in delete_by_index:
        del tmp_list[index - deleted_items]
        deleted_items +=1
    return tmp_list

#returning 7 if color equals white else 0
def getYByColor(color):
    if color == "white":
        return 7
    return 0

#checking if castelling is doable for the players
def isCastelling(color , arr_char):
    canSmall = False
    canBig = False
    y = getYByColor(color)
    if isLocationOpen((5,y) ,arr_char) and isLocationOpen((6,y) ,arr_char):
        canSmall = True
    if isLocationOpen((1,y) ,arr_char) and isLocationOpen((2,y) ,arr_char) and isLocationOpen((3,y) ,arr_char):
        canBig = True
    RightRook = getRightRook(color , arr_char)
    LeftRook = getLeftRook(color , arr_char)
    if getKing(color ,arr_char).getIsMoved() == True:
        return "cant"
    elif canBig and canSmall and LeftRook is not None and RightRook is not None and RightRook.getIsMoved() == False and LeftRook.getIsMoved() == False:
        return "big small"
    elif canSmall and RightRook is not None and RightRook.getIsMoved() == False:
        return "small"
    elif canBig and LeftRook is not None and LeftRook.getIsMoved() == False:
        return "big"
    return "cant"

#a function that is getting all of the castelling moving options and returning array of them
def getMovingInCastelling(king , currentPiece):
    castelling = isCastelling(currentPiece.getColor() , arr_char)
    castelingLocations = []
    print(castelling)
    if castelling == "big small":
        castelingLocations.append((king.getX() + 2 , king.getY()))
        castelingLocations.append((king.getX() - 2 , king.getY()))
    elif castelling == "big":
        castelingLocations.append((king.getX() - 2 , king.getY()))
    elif castelling == "small":
        castelingLocations.append((king.getX() + 2 , king.getY()))
    return castelingLocations


#a function that returns the right rook (the one for the small castelling)
def getRightRook(color , arr_char):
    for i in range(len(arr_char)):
        if arr_char[i].getColor() == color and arr_char[i].getType() == "rook" and arr_char[i].getX() == 7:
            return arr_char[i]
    return None

#a function that returns the left rook (the one for the big castelling)
def getLeftRook(color , arr_char):
    for i in range(len(arr_char)):
        if arr_char[i].getColor() == color and arr_char[i].getType() == "rook" and arr_char[i].getX() == 0:
            return arr_char[i]

#a function that returns true if there is checkMate else returns false
def isCheckMate():
    king = getKing(TURN , arr_char)
    if king == None:
        return None
    isMate = True
    for i in range(len(arr_char)):
        list = updateMove(arr_char[i] , king)
        if list!=None:
            arr_char[i].setArrMoveOptions(list)
            if len(arr_char[i].getArrMoveOptions()) > 0:
                isMate = False
    return isMate

#a function that gets a list as argument and returns a list with the valid places that the piece can go
def getValidPositions(list , current_piece , king):
    #counting the amount of items that got deleted
    deleted_items = 0
    delete_by_index = []
    for i in range(len(list)):
        if not canMove(current_piece , arr_char , list[i] , king):
            delete_by_index.append(i)
    for index in delete_by_index:
        del list[index - deleted_items]
        deleted_items +=1
    return list

#returns the pawn that reached the other end, retrun None if didn't reach the end
def getEndPawn(arr_char):
    for i in range(len(arr_char)):
        if arr_char[i].getType() == "pawn" and (arr_char[i].getY() == 0 or arr_char[i].getY() == 7):
            return arr_char[i]
    return None

#a function that get the places of the squre and returns the cordinates of top left
def getTopLeftCords(board_side , place , depth_x , depth_y):
    sqr_side = (board_side / 8)
    x = depth_x + sqr_side * place[0]
    #times 2 because he is currently at 6 and didn't
    y = depth_y + sqr_side * place[1]
    return (x,y)

#draws the drop menu for choosing options to switch characters when pawn reaches the other side
def drawPawnReachedTheEnd(pawn , board_side, depth_x , depth_y , board_size , dict_value_object):
    #if somehow the pawn is not at the end
    if pawn.getY() != 7 and pawn.getY() !=0:
        return None
    #getting all the positions to print
    arr_choosing = []
    print(pawn.getX() , pawn.getY())
    if pawn.getY() == 7:
        for i in range(4):
            arr_choosing.append((pawn.getX() , pawn.getY() - i))
    else:
        for i in range(4):
            arr_choosing.append((pawn.getX() , pawn.getY() + i))
    for i in range(len(arr_choosing)):
        print(arr_choosing[i])
        x , y = int(getTopLeftCords(board_side , arr_choosing[i], depth_x , depth_y)[0]), int(getTopLeftCords(board_side , arr_choosing[i], depth_x , depth_y)[1])
        pygame.draw.rect(window , (255,255,255) , (x , y , (BOARD_SIDE / 8) , (BOARD_SIDE / 8)))
        char = pygame.image.load(f"pictures/{pawn.getColor()}_{dict_value_object[i]}.png")
        char = pygame.transform.scale(char , CHAR_SIZE)
        window.blit(char, (x,y))
        pygame.display.flip()
    return arr_choosing


def main():
    #creation of objects
    creation()
    #update the screen with the values every few frames
    update(board, window, arr_char, BOARD_SIZE , DEPTH_X , DEPTH_Y , None , None, None , None)
    #what happens on screen
    #set the current working piece
    currentPiece = None 
    #a list that contains the choosing options when the pawn reaches the other side
    arr_choosing_switch = []
    #a boolean that tells if we are currently in a situation where a pawn reached the other side
    isPawnInOtherSide = False
    #dictionary of value to object, when an object reaches the other side
    dict_value_object = {0 : "queen" , 1 : "knight" , 2 : "rook" , 3 : "bishop"}
    #the pawn that reached the end
    endPawn = None
    #when it switches the click
    isOldClick = True
    
    #set the loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        global MOUSE_PRESSED , TURN , OPTIONS_EAT
        
        #get on click from user, when pawn reaches the other side
        if isPawnInOtherSide:
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:
                if isOldClick:
                    continue
            else:
                if isOldClick:
                    isOldClick = False
            print(mouse_pressed)
            if mouse_pressed[0] == True and isOldClick == False:
                position = mouse_sqr(DEPTH_X , DEPTH_Y , BOARD_SIDE)
                print(position)
                if position in arr_choosing_switch:
                    index = arr_choosing_switch.index(position)
                    print(dict_value_object[index])
                    endPawn.setType(dict_value_object[index])
                    arr_choosing_switch=[]
                    isPawnInOtherSide=False
                    endPawn = None
                    if currentPiece.getIsMoved() == False:
                        currentPiece.setIsMoved(True)
                    TURN = switchTurn(TURN)
                    currentPiece = None
                    update(board, window, arr_char, BOARD_SIZE , DEPTH_X , DEPTH_Y , currentPiece , is_moved , OPTIONS , OPTIONS_EAT)
                    is_moved = True
                    isOldClick = True
                    print("continue")
                    continue
            else:
                continue
        
        #a boolean expression that tells if I should update in ui
        should_update = False
        is_moved = False
        #checking if there is check
        king_turn = getKing(TURN, arr_char)
        updateOptionsEat(arr_char , king_turn)
        is_check = (isCheck(arr_char , TURN))
        # checking check mate
        if(is_check):
            isMate = isCheckMate()
            if isMate == None:
                print("[SYSTEM] an error has ocurred")
            elif isMate:
                #printing a winning msg
                opp_color = getOppositeColor(TURN)
                print(f"game over, {opp_color} wins!")
                sleep(5)
                return
        
        #current piece is the one you see where it can move
        #piece is the one the current piece can eat
        if (check_pressed_mouse(MOUSE_PRESSED) == "pressed"):
            piece = getPieceByPlace(DEPTH_X , DEPTH_Y , BOARD_SIDE)
            #clicked on the piece with the same color as turn, and set that it got clicked and that this is the piece that the player wants to move
            if piece != None and TURN == piece.getColor():
                #if clicked again on the same piece that was clicked it cancels it
                if piece.getIsClicked() == True:
                    piece.setIsClicked()
                    currentPiece = None
                    OPTIONS = []
                    should_update = True
                #if clicking on another piece is swithches to it (as shouing its options).
                else:
                    currentPiece = piece
                    should_update = True
                    OPTIONS , OPTIONS_EAT = getPlaces(piece , arr_char)
                    #checking for casteling and adding their locations to an array of all the casteling locations and to all moving options
                    castelingLocations = getMovingInCastelling(king_turn , currentPiece)
                    OPTIONS += castelingLocations
                    #get only the valid places of the piece to go to
                    OPTIONS = getValidPositions(OPTIONS , currentPiece , king_turn)
                    OPTIONS_EAT = getValidPositions(OPTIONS_EAT , currentPiece , king_turn)
                    already_clicked(arr_char)
                    piece.setIsClicked()

            #clicked on the player and then on another spot (empty or to eat)
            elif currentPiece!=None:
                future_pos = mouse_sqr(DEPTH_X , DEPTH_Y , BOARD_SIDE)
                #checking if he clicked on a player to eat, if yes it disappear the player
                if piece!=None and piece.getColor() != TURN and TURN == currentPiece.getColor():
                    if (future_pos in OPTIONS_EAT):
                        eat_peace = getPieceByLocation(future_pos , arr_char)
                        eat_peace.setX(None)
                        eat_peace.setY(None)
                #if clicked on a player to eat or on another spot on the board it moves the piece of the current turn
                if ((currentPiece!=None and piece!=None and piece.getColor() != TURN and TURN == currentPiece.getColor() and future_pos in OPTIONS_EAT) or (future_pos in OPTIONS and currentPiece!=None and piece == None)):
                    #play the sound
                    if future_pos in OPTIONS:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/move.wav'))
                    else:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/capture.wav'))
                    currentPiece.setY(future_pos[1])
                    currentPiece.setX(future_pos[0])
                    if future_pos in castelingLocations:
                        if future_pos[0] == 6:
                            Rook = getRightRook(TURN , arr_char)
                            Rook.setX(currentPiece.getX() - 1)
                        else:
                            Rook = getLeftRook(TURN , arr_char)
                            Rook.setX(currentPiece.getX() + 1)
                    #getting the pawn that reched the end
                    endPawn = getEndPawn(arr_char)
                    if endPawn is not None:
                        arr_choosing_switch = drawPawnReachedTheEnd(endPawn , BOARD_SIDE, DEPTH_X , DEPTH_Y , BOARD_SIZE , dict_value_object)
                        isPawnInOtherSide = True
                        """choice = input("enter what you want to be ")
                        while choice not in ["queen" , "rook" , "knight" , "bishop"]:
                            choice = input("invalid answer, enter what you want to be ")
                        endPawn.setType(choice)"""
                        continue
                    if currentPiece.getIsMoved() == False:
                        currentPiece.setIsMoved(True)
                    TURN = switchTurn(TURN)
                    currentPiece = None
                    should_update = True
                    is_moved = True
            MOUSE_PRESSED = True
        elif (check_pressed_mouse(MOUSE_PRESSED) == "not pressed"):
            MOUSE_PRESSED = False
        
        #update the screen
        if should_update:
            #update the places of the players on the screen by their values
            update(board, window, arr_char, BOARD_SIZE , DEPTH_X , DEPTH_Y , currentPiece , is_moved , OPTIONS , OPTIONS_EAT)
        #clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()