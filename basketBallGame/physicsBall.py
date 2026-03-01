#imports
import pygame, math , time , random

#set clock and time
clock = pygame.time.Clock()
t0=time.time()

#define screen
window_size = (800 * 1.5, 600 * 1.5)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("My Pygame Window")

#BasketBall object class
class BasketBall:
   def __init__(self, basketBall_x, basketBall_y, radius):
      self.basketBall_x = basketBall_x
      self.basketBall_y = basketBall_y
      self.radius = radius
      self.speed_y = 0
      self.speed_x = 0
   def getX(self):
      return self.basketBall_x
   def getY(self):
      return self.basketBall_y
   def setX(self , new_x):
      self.basketBall_x = new_x
   def setY(self , new_y):
      self.basketBall_y = new_y
   def getRadius(self):
      return self.radius
   def getSpeedY(self):
      return self.speed_y
   def changeSpeedY(self , pace):
      self.speed_y+=pace
   def changeSpeedX(self , pace):
      self.speed_x+=pace
   def getSpeedX(self):
      return self.speed_x
   def changeX(self):
      self.basketBall_x += self.speed_x
   def changeY(self):
      self.basketBall_y += self.speed_y
   def setSpeedX(self, speed):
      self.speed_x = speed
   def setSpeedY(self, speed):
      self.speed_y = speed

   #is touching the BasketBall
   def touchingBasketBall(self):
      if (self.is_mouse_on_ball(pygame.mouse.get_pos()) and check_pressed_mouse()):
         self.setSpeedX(0)
         self.setSpeedY(0)
         return True
      else: 
         return False
   
   #if touching walls
   def isTouchingWalls(self , win_max_x , win_max_y):
      return_value = False
      if ((self.basketBall_x + self.radius) >= win_max_x or (self.basketBall_x - self.radius) <= 0):
         self.reverseDirection('x')
         if (self.basketBall_x + self.radius) >= win_max_x:
            self.setX(win_max_x - self.radius)
         else:
            self.setX(self.radius)
         return_value = True
      if((self.basketBall_y + self.radius) >= win_max_y or (self.basketBall_y - self.radius) <= 0):
         self.reverseDirection('y')
         if (self.basketBall_y + self.radius) >= win_max_y:
            self.setY(win_max_y - self.radius)
         else:
            self.setY(self.radius)
         return_value = True
      return return_value
   
   def isTouchingGroand (self , win_max_y):
      if((self.basketBall_y + self.radius) >= win_max_y):
         return True
      return False
   
   #bounce of the wall
   def reverseDirection(self, dir):
      if dir == 'y':
         changeByValueY = 0.15 * self.speed_y
         if (self.speed_y < 0.2 and self.speed_y > 0):
            self.setSpeedY(0)
            return 
         basketBall.setSpeedY(-basketBall.speed_y)
         basketBall.changeSpeedY(changeByValueY)
      if dir == 'x':
         changeByValueX = 0.15 * basketBall.speed_x
         basketBall.setSpeedX(-basketBall.speed_x)
         basketBall.changeSpeedX(changeByValueX)

   #if touch the basketBall make it follow mouse
   def makeTheBallFollow(self , win_max_x , win_max_y):
      if (self.touchingBasketBall()):
         self.setX(pygame.mouse.get_pos()[0])
         self.setY(pygame.mouse.get_pos()[1])
         limitedArea(win_max_x , win_max_y)

   #check collision between mouse and ball
   def is_mouse_on_ball(self , posMouse):
      mouse_x = posMouse[0]
      mouse_y = posMouse[1]
      side_a = only_positive(mouse_x-self.basketBall_x)
      side_b = only_positive(mouse_y-self.basketBall_y)
      if (math.sqrt(self.radius*self.radius)>=math.sqrt(side_a*side_a + side_b*side_b)):
        return True
      return False

#click listenter
def check_pressed_mouse():
   mouse_pressed = pygame.mouse.get_pressed()
   if mouse_pressed[0]:
      return True

#erach muchlat
def only_positive(x):
   if (x>0):
      return x
   return (-x)

# calculate mouse speed and return a tuple "speed" of (x , y)
def calculate_mouse_speed(last_x, last_y):
   current_x = pygame.mouse.get_pos()[0]
   current_y = pygame.mouse.get_pos()[1]
   pace_x = float(current_x) - float(last_x)
   pace_y = float(current_y) - float(last_y)
   return (pace_x , pace_y)


#Set values
basketBall = BasketBall(400, 300, 35)
GRAVITY = 0.001
counter_to_mouse_speed = 0
mouse_speed_frame_rate = 5
last_x = basketBall.getX()
last_y = basketBall.getY()
is_released = False
lastFramePos = (basketBall.getX() , basketBall.getY())
is_during_a_bucket = False

#bounce
#check positivity
def isPositive(num):
   if num>=0:
      return True
   return False

#turn minos to plus and the other way
def turnToOpposite(num):
   if(num>0):
      num-=2*num
      return num
   else:
      num-=2*(num)
      return num



#Don't let the mouse lead it to far
def limitedArea(win_max_x , win_max_y):
   if (basketBall.getX() > win_max_x - basketBall.getRadius()):
      basketBall.setX(win_max_x - basketBall.getRadius())
   if (basketBall.getY() > win_max_y - basketBall.getRadius()):
      basketBall.setY(win_max_y - basketBall.getRadius())
   if (basketBall.getX() < basketBall.getRadius()):
      basketBall.setX(0 + basketBall.getRadius())
   if (basketBall.getY() < basketBall.getRadius()):
      basketBall.setY(0 + basketBall.getRadius())

#if 2 balls collide
def collideRimBall(center1 , center2 , r1 , r2):
   sideA = only_positive(center1[0]-center2[0])
   sideB = only_positive(center1[1]-center2[1])
   if (math.sqrt((r1 + r2) * (r1 + r2)) >= math.sqrt(sideA * sideA + sideB * sideB)):
      return True
   return False



#hoop object class
class Hoop:
   def __init__(self, length , rangeOfHeight, radiusOfHoopCorner , distanceFromTheWall):
      self.distanceFromTheWall = distanceFromTheWall
      self.rangeOfHeight = rangeOfHeight
      self.length = length
      self.height = random.randint(rangeOfHeight[0] , rangeOfHeight[1])
      self.radiusOfHoopCorner = radiusOfHoopCorner
   def getDistanceFromTheWall(self):
      return self.distanceFromTheWall
   def setDistanceFromTheWall (self , distanceFromTheWall):
      self.distanceFromTheWall = distanceFromTheWall
   def getRadiusOfHoopCorner(self):
      return self.radiusOfHoopCorner
   def setRadiusOfHoopCorner(self, radiusOfHoopCorner):
      self.radiusOfHoopCorner = radiusOfHoopCorner
   def getLength(self):
      return self.length
   def getHeight(self):
      return self.height
   def setHeight(self , height):
      self.height = height
   def setLength(self , length):
      self.length = length
   def changeHeight(self):
      self.height = random.randint(self.range[0] , self.range[1])
   
   def calculateyCordinatesOfHoopLeft(self , window_frame):
      return (window_frame[0]-self.getLength()-self.getDistanceFromTheWall() - 3 * self.getRadiusOfHoopCorner(), self.getHeight())
   
   def calculateyCordinatesOfHoopRight(self , window_frame):
      return (window_frame[0]-self.getDistanceFromTheWall() - self.getRadiusOfHoopCorner() , self.getHeight())
   
   #do what needed in collidenes
   def ifCollide(self , bBall , window_frame):
      #print(self.calculateyCordinatesOfHoopRight(window_frame))
      if ((collideRimBall((bBall.getX(), bBall.getY()) , self.calculateyCordinatesOfHoopLeft(window_frame) , bBall.getRadius() , hoop.getRadiusOfHoopCorner()))):
         bBall.reverseDirection('x')
         bBall.reverseDirection('y')
         if (bBall.getX() > self.calculateyCordinatesOfHoopLeft(window_frame)[0]):
            bBall.changeSpeedX(0.1)
         elif (bBall.getX() < self.calculateyCordinatesOfHoopLeft(window_frame)[0]):
            bBall.changeSpeedX(-0.1)
      if ((collideRimBall((bBall.getX(), bBall.getY()) , self.calculateyCordinatesOfHoopRight(window_frame) , bBall.getRadius() , hoop.getRadiusOfHoopCorner()))):
         bBall.reverseDirection('x')
         bBall.reverseDirection('y')
         if (bBall.getX() > self.calculateyCordinatesOfHoopRight(window_frame)[0]):
            bBall.changeSpeedX(0.1)
         elif (bBall.getX() < self.calculateyCordinatesOfHoopRight(window_frame)[0]):
            bBall.changeSpeedX(-0.1)
   
   def whileHoldingBallCollide (self , bBall , window_frame):
      if (collideRimBall((bBall.getX() , bBall.getY()) , self.calculateyCordinatesOfHoopLeft(window_frame) , bBall.getRadius() , self.getRadiusOfHoopCorner())):
         cordinates = getGoodCordinates(bBall , self.calculateyCordinatesOfHoopLeft(window_frame) , self.getRadiusOfHoopCorner())
         pygame.draw.circle(window , (255,255,255) , (cordinates[0] , cordinates[1]) , 1)
         bBall.setX(cordinates[0])
         bBall.setY(cordinates[1])
      # need "if" if rim is to small 
      elif (collideRimBall((bBall.getX() , bBall.getY()) , self.calculateyCordinatesOfHoopRight(window_frame) , bBall.getRadius() , self.getRadiusOfHoopCorner())):
         cordinates = getGoodCordinates(bBall , self.calculateyCordinatesOfHoopRight(window_frame) , self.getRadiusOfHoopCorner())
         pygame.draw.circle(window , (255,255,255) , (cordinates[0] , cordinates[1]) , 1)
         bBall.setX(cordinates[0])
         bBall.setY(cordinates[1])
   

   #fix it it is not perfect!
   def checkBucket(self, bBall, isTouchingBasketBall, window_size , lastFramePos , is_during_a_bucket_local):
      #print (isTouchingBasketBall == False , bBall.getX() > (self.calculateyCordinatesOfHoopLeft(window_size)[0] + self.getRadiusOfHoopCorner()) , bBall.getX() < (self.calculateyCordinatesOfHoopRight(window_size)[0] - self.getRadiusOfHoopCorner()) , bBall.getY() == self.getHeight())
      # check if getting into the basket rn
      #if touching the ball that means basket does not count
      if isTouchingBasketBall == True:
         return "touch" , is_during_a_bucket_local
      #if is not during a basket and in rim range and
      if (is_during_a_bucket == False and (bBall.getY() + bBall.getRadius()) >= (self.getHeight() - self.getRadiusOfHoopCorner()) and (bBall.getY() + bBall.getRadius()) <= (self.getHeight() + self.getRadiusOfHoopCorner()) and (bBall.getX() - bBall.getRadius()) >= (self.calculateyCordinatesOfHoopLeft(window_size)[0] + self.getRadiusOfHoopCorner()) and (bBall.getX() + bBall.getRadius()) <= (self.calculateyCordinatesOfHoopRight(window_size)[0] - self.getRadiusOfHoopCorner())):
         is_during_a_bucket_local = True
         return "dont know" , is_during_a_bucket_local
      #if the ball is not in the rim's range that means it is not during a bucket
      elif (((bBall.getX() - bBall.getRadius()) >= (self.calculateyCordinatesOfHoopLeft(window_size)[0] + self.getRadiusOfHoopCorner()) and (bBall.getX() + bBall.getRadius()) <= (self.calculateyCordinatesOfHoopRight(window_size)[0] - self.getRadiusOfHoopCorner())) == False):
         is_during_a_bucket_local = False
         return "no" , is_during_a_bucket
      #if the ball is during a bucket and the ball got down that means it is a bucket
      elif (is_during_a_bucket == True and (bBall.getY() - bBall.getRadius()) >= (self.getHeight() + self.getRadiusOfHoopCorner())):
         is_during_a_bucket_local = False
         return "yes" , is_during_a_bucket_local
      return "None" , is_during_a_bucket_local
      
   def checkBucketNew(self, bBall,  isTouchingBasketBall, window_size , is_during_a_bucket_local):
         if isTouchingBasketBall == True:
            return "touch" , False
         elif (is_during_a_bucket_local == False and ((bBall.getY() + bBall.getRadius()) >= self.getHeight()) and ((bBall.getY() - bBall.getRadius()) <= self.getHeight()) and ((bBall.getX() + bBall.getRadius()) > (self.calculateyCordinatesOfHoopLeft(window_size)[0] - self.getRadiusOfHoopCorner())) and (bBall.getX() + bBall.getRadius()) < (self.calculateyCordinatesOfHoopRight(window_size)[0] + self.getRadiusOfHoopCorner())):
            is_during_a_bucket_local = True
            return "during a bucket..." , is_during_a_bucket_local
         elif (((bBall.getX() + bBall.getRadius()) > (self.calculateyCordinatesOfHoopLeft(window_size)[0] - self.getRadiusOfHoopCorner())) and (bBall.getX() + bBall.getRadius()) < (self.calculateyCordinatesOfHoopRight(window_size)[0] + self.getRadiusOfHoopCorner()) == False):
            is_during_a_bucket_local = False
            return "not is a bucket" , is_during_a_bucket_local
         elif (is_during_a_bucket_local == True and (bBall.getY() - bBall.getRadius()) > self.getHeight()):
            is_during_a_bucket_local = False
            return "yes" , is_during_a_bucket_local
         return "None" , is_during_a_bucket_local

            





   '''if (isTouchingBasketBall == False and bBall.getX() > (self.calculateyCordinatesOfHoopLeft(window_size)[0] + self.getRadiusOfHoopCorner()) and bBall.getX() < (self.calculateyCordinatesOfHoopRight(window_size)[0] - self.getRadiusOfHoopCorner()) and ((lastFramePos[1] < self.getHeight() and bBall.getY() == self.getHeight()) or (lastFramePos[1] < self.getHeight() and bBall.getY() > self.getHeight()))):
         return True
      return False'''

def getGoodCordinates(bBall , rimCords , rimR):
   sideX = rimCords[0] - bBall.getX()
   sideY = rimCords[1] - bBall.getY()
   pit = math.sqrt(sideX * sideX + sideY * sideY)
   sideA2X = ((bBall.getRadius() + rimR) / pit) * sideX
   sideB2Y = ((bBall.getRadius() + rimR) / pit) * sideY
   
   return (rimCords[0] - sideA2X , rimCords[1] - sideB2Y)
         


#Hoop itself
hoop = Hoop((basketBall.getRadius() * 2) * 2,(200 , 400) , 4 , 20)

#what happens on screen
running = True
while running:
   # Handle events
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
   #check collideness
   hoop.whileHoldingBallCollide(basketBall , window_size)
   # Draw shapes
   window.fill((0, 0, 0))
   pygame.draw.circle(window , (255,165,0) , (basketBall.getX(), basketBall.getY()) ,basketBall.getRadius())
   
   #reminder: add to class min max of hoop
   pygame.draw.circle(window , (255,255,255) , (window_size[0]-hoop.getLength()-hoop.getDistanceFromTheWall() - 3 * hoop.getRadiusOfHoopCorner(), hoop.getHeight()) , hoop.getRadiusOfHoopCorner())
   pygame.draw.circle(window , (255,255,255) , (window_size[0]-hoop.getDistanceFromTheWall() - hoop.getRadiusOfHoopCorner(), hoop.getHeight()) , hoop.getRadiusOfHoopCorner())
   
   #check touching
   isTouchingBasketBall = basketBall.touchingBasketBall()
   isTouchingGroand = basketBall.isTouchingGroand(window_size[1])

   #check bucket
   printT , is_during_a_bucket= hoop.checkBucketNew(basketBall , isTouchingBasketBall , window_size , is_during_a_bucket)
   '''print(f"{printT}")'''
   if printT == "yes":
      print("u r bucket!")
      
   isInCorner = basketBall.isTouchingWalls(window_size[0], window_size[1])    
   #note: if (isTouchingBasketBall==True or isInCorner==False)
   #gravity
   if (isTouchingBasketBall==True or isTouchingGroand==False):
      basketBall.changeSpeedY(GRAVITY)
   
   #what happens if rim touch
   hoop.ifCollide(basketBall , window_size)

   #when mouse is touching the ball it makes the ball follow the mouse without escaping the borders
   basketBall.makeTheBallFollow(window_size[0], window_size[1])
   
   #save last position of the ball , and calculate mouse's speed 
   if (counter_to_mouse_speed % mouse_speed_frame_rate == 0):
      mouse_speed = calculate_mouse_speed(last_x , last_y)
      last_x = pygame.mouse.get_pos()[0]
      last_y = pygame.mouse.get_pos()[1]

   # check if just released
   if (is_released == True and isTouchingBasketBall == False):
      basketBall.changeSpeedX(mouse_speed[0]/15)
      basketBall.changeSpeedY(mouse_speed[1]/15)

   #last frame pos
   lastFramePos = (basketBall.getX() , basketBall.getY())

   #change the place due to speed
   basketBall.changeY()
   basketBall.changeX()
   
   

   #add one to counter every frame rate
   counter_to_mouse_speed+=1

   #change is_released to current status of holding bball
   is_released = isTouchingBasketBall
   
   #clock.tick(60)
   pygame.display.flip()
   
pygame.quit()