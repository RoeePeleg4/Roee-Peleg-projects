import pygame
from sys import exit
import time
import random

faster = 0
was_there = False 
basic_time=1600
def change_velocity(time):
    global was_there , basic_time
    if (time!=0 and time%10==0 and was_there == False):
        was_there = True
        if (basic_time>500):
            basic_time-=200
    elif time%10!=0:
        was_there = False
    return basic_time


def obstacleMovment(lst , time): 
    global faster
    if lst:
        for i in range(len(lst)-1):
            if (time%10==0 and int(time)/10!=faster):
                faster +=0.5
            obst_rect = lst[i][0]
            if ((4 + faster)<=10):
                obst_rect.x -=(4 + faster)
            if (lst[i][1]=="fly"):
                screen.blit(fly_surf , obst_rect)  
            else:
                screen.blit(snail_surf , obst_rect)
        return lst  
    else: 
        return []
def cleanList(list):
    if list:
        for i in range (len(list)-1):
            obst_rect = list[i][0]
            if obst_rect.right<0:
                list.pop(i)
pygame.init()
screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("the roee")
clock = pygame.time.Clock()
game_is_on = True

#set music
jump_song = pygame.mixer_music.load('audio/jump.mp3')
theme_song = pygame.mixer_music.load('audio/music.wav''')
pygame.mixer_music.set_volume(0.2)

#obsticales
snail_surf = pygame.transform.scale(pygame.image.load('graphics\snail\snail1.png'),(72,36))
fly_surf = pygame.transform.scale(pygame.image.load('graphics\Fly\Fly1.png'''),(84,40))
obstacle_rect_list = []
#set surfeses
player_surf = pygame.transform.scale(pygame.image.load('graphics\Player\player_stand.png'''), (68,84))
ground = pygame.transform.scale(pygame.image.load('graphics\ground.png'''),(800,100))
sky = pygame.transform.scale(pygame.image.load('graphics\sky.png'''),(800,400))

#set rectangles
rect_player = player_surf.get_rect(bottomleft = (10, 400))

#player jumps
currently_jumping = False
many_jumps = 0
currently_up = False
currenly_down = False
#audio
pygame.mixer.Channel(1).set_volume(0.2)
pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio\music.wav'''))

fps_counter = 0
#draw text
font = pygame.font.Font('font\Pixeltype.ttf''' , 100)
def draw_txt(text,font ,  color , x , y):
    img = font.render(text , True , color)
    screen.blit(img , (x,y))

#button
font_button = pygame.font.Font('font\Pixeltype.ttf''' , 50)
surf = font_button.render('Restart' , True , 'black')
button = pygame.Rect(250,200,125,40)

#change the screen 
def change_rect (obstacle_rect_list):
    for i in range(len(obstacle_rect_list)):
        rect = obstacle_rect_list[i][0]
        if (obstacle_rect_list[i][1] == "fly"):
            screen.blit(fly_surf , rect)
        else:
            screen.blit(snail_surf , rect)


#plyer walking position 
current_walk = 1
player_surf = pygame.transform.scale(pygame.image.load('graphics\Player\player_walk_1.png'''), (68,84))
t0=time.time()

#timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer , 1400)

while True:
    #get the events
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #timer
            if event.type == enemy_timer and game_is_on:
                pygame.time.set_timer(enemy_timer , time_to_spawn)
                rnd_num = random.randint(0,2)
                if rnd_num == 0:
                    obstacle_rect_list.append((fly_surf.get_rect(midbottom = (random.randint(900, 1100),300)) , "fly"))
                else:
                    obstacle_rect_list.append((snail_surf.get_rect(midbottom = (random.randint(900, 1100),400)) , "snail"))

                
    pygame.display.update()
    if game_is_on:
        fps_counter += 1
        #back_ground set
        screen.blit(ground,(0,400))
        
        screen.blit(sky,(0,0))
        #timer score
        current_time = (str(time.time()-t0))[:3]
        if ((time.time()-t0)>10):
            current_time = (str(time.time()-t0))[:4]
        elif ((time.time()-t0)>100):
            current_time = (str(time.time()-t0))[:5]
        draw_txt(current_time , font , "black" , 20 , 20)
        #foword position
        #charcters position now
        #screen.blit(main_char,(5,316))

        #obstcacle Movment
        time_to_spawn = change_velocity(float(current_time))
        obstacle_rect_list=obstacleMovment(obstacle_rect_list , float(current_time))
        cleanList(obstacle_rect_list)
        
        #jump the character
        jump_amount = 30
        #character jumping
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and (currently_jumping == False):
            player_surf = pygame.transform.scale(pygame.image.load('graphics\Player\jump.png'''), (68,84))
            pygame.mixer.Channel(0).set_volume(0.3)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('audio\jump.mp3'''))
            currently_jumping = True
            currently_up = True
        
        #jump
        if currently_jumping:
            if currently_up:
                rect_player.top -=6
                many_jumps +=1
            elif currenly_down:
                rect_player.top +=6
                many_jumps +=1
        if currently_up:
            if many_jumps == jump_amount:
                currently_up = False
                currenly_down = True
                many_jumps = 0
        elif currenly_down:
            if many_jumps == jump_amount:
                currenly_down = False
                currently_jumping = False
                many_jumps= 0
        #update char position
        screen.blit(player_surf , rect_player)
        
        #check if lost
    
        for i in range(len(obstacle_rect_list)-1):
            rect = obstacle_rect_list[i][0]
            if (rect_player.colliderect(rect)):
                game_is_on = False

        #max fps
        if fps_counter%25==0:
            if (currently_jumping==False):
                if (current_walk == 1):
                    fly_surf = pygame.transform.scale(pygame.image.load('graphics\Fly\Fly1.png'''),(84,40))
                    snail_surf = pygame.transform.scale(pygame.image.load('graphics\snail\snail1.png'''),(72,36))
                    change_rect(obstacle_rect_list)
                    player_surf = pygame.transform.scale(pygame.image.load('graphics\Player\player_walk_2.png'''), (68,84))
                    current_walk=0
                else:
                    snail_surf = pygame.transform.scale(pygame.image.load('graphics\snail\snail2.png'''),(72,36))
                    fly_surf = pygame.transform.scale(pygame.image.load('graphics\Fly\Fly2.png'''),(84,40))
                    change_rect(obstacle_rect_list)
                    player_surf = pygame.transform.scale(pygame.image.load('graphics\Player\player_walk_1.png'''), (68,84))
                    current_walk=1  
    else:
        draw_txt("Game Over", font , "black" , 250 , 100)
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if button.collidepoint(event.pos):
                #restart the game
                faster = 0
                game_is_on = True
                obstacle_rect_list=[]
                t0 = time.time()
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('audio\music.wav'''))
        x_click , y_click = pygame.mouse.get_pos()
        if button.x <= x_click <= (button.x + 110) and button.y <= y_click <= (button.y +60):
            pygame.draw.rect(screen,(87,183,212),button )
        else:
            pygame.draw.rect(screen, (115,222,255),button)
        screen.blit(surf,(button.x +5, button.y+5))
    clock.tick(60)