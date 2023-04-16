# For getting a action we need 
# obstacle ->  lower left and lower right corner corridinates 
# own car -> upper left and upper right corner coordinates
# road ->    left and right coordinate


import numpy as np
import torch
import random
from collections import deque
from game_AI import Game
from model import Linear_QNet, QTrainer


MAX_MEMORY  = 100_000
BATCH_SIZE = 1000
LR = 0.0005

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.k = []
        self.memory = deque(maxlen = MAX_MEMORY)
        self.model = Linear_QNet(5,64,3)
        self.trainer = QTrainer(self.model,LR,self.gamma)
         
        
    def get_action(self,state):
        # Epsilon greedy approach
        self.epsilon = 50 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
            self.k.append(0)
        else:
            self.k.append(1)
            state0 =  torch.tensor(np.array(state), dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
                
        return final_move

    def train_short_memory(self,state,action,reward,next_state,g_o):
        self.trainer.train_step(state,action,reward,next_state,g_o)
    
    
    def remember(self,state,action,reward,next_state,g_o):
        self.memory.append((state,action,reward,next_state,g_o))   


    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states,actions,rewards,next_states,g_os = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,g_os)        
        
def train():
    game = Game()
    agent = Agent()
    record = 0
   
    while True:
        #get current state
        state_old = game.get_state()
        
        # get action or move
        move = agent.get_action(state_old)
        
        # perform move and get new state
        reward,g_o,score = game.play_step(move)
        next_state = game.get_state()
        
        #train short memory
        agent.train_short_memory(state_old,move,reward,next_state,g_o)
        
        #remember
        agent.remember(state_old,move,reward,next_state,g_o)
        
        if g_o:
            game.__init__()
            agent.n_games+=1
            agent.train_long_memory()
            
            if score > record:
                record =score
            agent.model.save()
           
            print("Game ", agent.n_games,' Scores ', score , ' Records: ',record, ' Epsilon: ' , agent.epsilon)
                    
            agent.k = []
           
              

if __name__ == '__main__':
    train()
