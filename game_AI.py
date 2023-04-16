import pygame
import random
import numpy as np
gray=(119,118,110)
black=(0,0,0)
red=(255,0,0)
green=(0,200,0)
blue=(0,0,200)
bright_red=(255,0,0)
bright_green=(0,255,0)
bright_blue=(0,0,255)
display_width=800
display_height=600

SPEED = 60

pygame.init()

carimg=pygame.image.load('images/car1.jpg')
backgroundpic=pygame.image.load("images/grass.jpg")
yellow_strip=pygame.image.load("images/yellow_strip.jpg")
strip=pygame.image.load("images/strip.jpg")
intro_background=pygame.image.load("images/background.jpg")
instruction_background=pygame.image.load("images/background2.jpg")
car_width=56

class Game:

    def __init__(self):
        self.gamedisplays=pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption("Car Game")
        self.x=(display_width*0.45)
        self.y=(display_height*0.8)
        self.x_change=0
        self.obstacle_speed=9
        self.obs=0
        self.obs_startx=random.randrange(200,(display_width-200))
        self.obs_starty=-750
        self.obs_width=56
        self.obs_height=125
        self.passed=0
        self.score=0
        self.reward = 0
        self.y2=7
        self.clock = pygame.time.Clock()

    def obstacle(self):
        if self.obs==0:
            obs_pic=pygame.image.load("images/car1.jpg")
        elif self.obs==1:
            obs_pic=pygame.image.load("images/car2.jpg")
        elif self.obs==2:
            obs_pic=pygame.image.load("images/car2.jpg")
        elif self.obs==3:
            obs_pic=pygame.image.load("images/car4.jpg")
        elif self.obs==4:
            obs_pic=pygame.image.load("images/car5.jpg")
        elif self.obs==5:
            obs_pic=pygame.image.load("images/car6.jpg")
        elif self.obs==6:
            obs_pic=pygame.image.load("images/car7.jpg")
        self.gamedisplays.blit(obs_pic,(self.obs_startx,self.obs_starty))

    def score_system(self):
        font=pygame.font.SysFont(None,25)
        text=font.render("Passed"+str(self.passed),True,black)
        score=font.render("Score"+str(self.score),True,red)
        self.gamedisplays.blit(text,(0,50))
        self.gamedisplays.blit(score,(0,30))

    # def crash(self):
    #     print(self.score,self.reward,False)
    #     pygame.quit()
    #     quit()

    def background(self):
        self.gamedisplays.blit(backgroundpic,(0,0))
        self.gamedisplays.blit(backgroundpic,(0,200))
        self.gamedisplays.blit(backgroundpic,(0,400))
        self.gamedisplays.blit(backgroundpic,(700,0))
        self.gamedisplays.blit(backgroundpic,(700,200))
        self.gamedisplays.blit(backgroundpic,(700,400))
        self.gamedisplays.blit(yellow_strip,(400,0))
        self.gamedisplays.blit(yellow_strip,(400,100))
        self.gamedisplays.blit(yellow_strip,(400,200))
        self.gamedisplays.blit(yellow_strip,(400,300))
        self.gamedisplays.blit(yellow_strip,(400,400))
        self.gamedisplays.blit(yellow_strip,(400,500))
        self.gamedisplays.blit(strip,(120,0))
        self.gamedisplays.blit(strip,(120,100))
        self.gamedisplays.blit(strip,(120,200))
        self.gamedisplays.blit(strip,(680,0))
        self.gamedisplays.blit(strip,(680,100))
        self.gamedisplays.blit(strip,(680,200))

    def car(self):
        self.gamedisplays.blit(carimg,(self.x,self.y))
    
    def get_state(self):
        # we have to return
        # distance of car from  wall
        # distance 1 of car from obstacle
        # distance 2 of car from obstacle
        
        return np.array([
            self.x-110,
            680-self.x,
            self.x,
            self.x+car_width,
            self.obs_startx,
            self.obs_startx+car_width,
            self.y -self.obs_starty-self.obs_height
        ],dtype=int) 
         
         
        # return np.array([self.x-110,
        #                  680-self.x,
        #                 self.x-self.obs_startx+car_width,
        #                 #  self.obs_starty+self.obs_height-self.y,
        #                 self.obs_startx-self.x-car_width
        #                 # ,self.obs_starty+125-self.y
        #                 ],dtype = int)
        # return np.array([self.x-110,680-self.x,self.obs_startx+car_width-self.x],dtype = int)
        

    def play_step(self,action):  
        # to be called after getting a output of neural network
        self.move(action)
        if self.x>690-car_width or self.x<110:
                self.reward = -10
                return self.reward,True,self.score 
            
        if self.x>display_width-(car_width+110) or self.x<110:
                self.reward = -10
                # pygame.quit()
                return self.reward,True,self.score 
                
        if self.obs_starty>display_height:
                self.obs_starty=0-self.obs_height
                self.obs_startx=random.randrange(170,(display_width-170))
                self.obs=random.randrange(0,7)
                self.passed=self.passed+1
                self.score+=10
                self.reward += 10
                if int(self.passed)%10==0:
                    self.obstacle_speed+=4
                    pygame.display.update()
        if self.y<self.obs_starty+self.obs_height:
                if self.x > self.obs_startx and self.x < self.obs_startx + self.obs_width or self.x+car_width > self.obs_startx and self.x+car_width < self.obs_startx+self.obs_width:
                    self.reward = -10
                    # pygame.quit()
                    return self.reward,True,self.score
        pygame.display.update()
        self.clock.tick(60)
        return self.reward,False,self.score
        
    def move(self,action):
        # action 
        # 0 - > no action
        # 1 -> move left
        # 2 -> move right
        if action[0] == 1:
            self.x = self.x
        elif action[1] == 1:
            self.x -= 5
        elif action[2] == 1:
            self.x += 5
        self.update_ui()
        self.y2+=self.obstacle_speed
        self.obs_starty-=(self.obstacle_speed/4)
        self.obstacle()
        self.obs_starty+=self.obstacle_speed
        self.car()
        self.score_system()
        
    
    
    def update_ui(self):
        self.gamedisplays.fill(gray)
        rel_y=self.y2%backgroundpic.get_rect().width
        self.gamedisplays.blit(backgroundpic,(0,rel_y-backgroundpic.get_rect().width))
        self.gamedisplays.blit(backgroundpic,(700,rel_y-backgroundpic.get_rect().width))
        if rel_y<800:
                self.gamedisplays.blit(backgroundpic,(0,rel_y))
                self.gamedisplays.blit(backgroundpic,(700,rel_y))
                self.gamedisplays.blit(yellow_strip,(400,rel_y))
                self.gamedisplays.blit(yellow_strip,(400,rel_y+100))
                self.gamedisplays.blit(yellow_strip,(400,rel_y+200))
                self.gamedisplays.blit(yellow_strip,(400,rel_y+300))
                self.gamedisplays.blit(yellow_strip,(400,rel_y+400))
                self.gamedisplays.blit(yellow_strip,(400,rel_y+500))
                self.gamedisplays.blit(yellow_strip,(400,rel_y-100))
                self.gamedisplays.blit(strip,(120,rel_y-200))
                self.gamedisplays.blit(strip,(120,rel_y+20))
                self.gamedisplays.blit(strip,(120,rel_y+30))
                self.gamedisplays.blit(strip,(680,rel_y-100))
                self.gamedisplays.blit(strip,(680,rel_y+20))
                self.gamedisplays.blit(strip,(680,rel_y+30))
        
    

#     def game_loop(self):
#         bumped=False
#         while not bumped:
#             for event in pygame.event.get():                          
#                 if event.type==pygame.QUIT:
#                     pygame.quit()
#                     quit()

#                 if event.type==pygame.KEYDOWN:
#                     if event.key==pygame.K_LEFT:
#                         self.x_change=-5
#                     if event.key==pygame.K_RIGHT:
#                         self.x_change=5
#                 if event.type==pygame.KEYUP:
#                     if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
#                         self.x_change=0

#             self.x+=self.x_change
#             self.update_ui()
#             self.y2+=self.obstacle_speed
#             self.obs_starty-=(self.obstacle_speed/4)
#             self.obstacle()
#             self.obs_starty+=self.obstacle_speed
#             self.car()
#             self.score_system()
#             if self.x>690-car_width or self.x<110:
#                 self.crash()
#             if self.x>display_width-(car_width+110) or self.x<110:
#                 self.crash()
#             if self.obs_starty>display_height:
#                 self.obs_starty=0-self.obs_height
#                 self.obs_startx=random.randrange(170,(display_width-170))
#                 self.obs=random.randrange(0,7)
#                 self.passed=self.passed+1
#                 self.score+=10
#                 self.reward += 1
#                 if int(self.passed)%10==0:
#                     self.obstacle_speed+4
#                     pygame.display.update()

#             if self.y<self.obs_starty+self.obs_height:
#                 if self.x > self.obs_startx and self.x < self.obs_startx + self.obs_width or self.x+car_width > self.obs_startx and self.x+car_width < self.obs_startx+self.obs_width:
#                     self.crash()
#             pygame.display.update()
#             self.clock.tick(60)

# if __name__ == '__main__':
#     game = Game()
#     game.game_loop()
#     # game.__init__()
#     # action_id = random.randint(0,2)
#     # action = [0,0,0]
#     # action[action_id] = 1
#     # _,g_o,_ = game.play_step(action)
#     # while ~g_o:
#     #     action = [0,0,0]
#     #     action_id = random.randint(0,2)
#     #     action[action_id] = 1
#     #     _,g_o,_ = game.play_step(action)
#     # # pygame.quit()
#     # quit()
