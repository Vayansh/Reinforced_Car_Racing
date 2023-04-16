
import numpy as np
import torch
import random
from collections import deque
from game_AI import Game
from model import Linear_QNet, QTrainer


def test():
    game = Game()
    model = Linear_QNet(5,64,3)
    model.load_state_dict(torch.load('model/model.pth'))
    record = 0
    games = 10
    # n_games = 0
    # total_scores = 0
    # plot_scores = []
    # plot_mean_scores =[]
    for _ in range(games):
        while True:
            #get current state
            state_old = game.get_state()
            
            # get action or move
            move = [0,0,0]
            state0 =  torch.tensor(np.array(state_old), dtype=torch.float)
            prediction = model(state0)
            f_move = torch.argmax(prediction).item()
            move[f_move] = 1
            
            # perform move and get new state
            _,g_o,score = game.play_step(move)
            # next_state = game.get_state()
            
            #train short memory
            # agent.train_short_memory(state_old,move,reward,next_state,g_o)
            
            #remember
            # agent.remember(state_old,move,reward,next_state,g_o)
            
            if g_o:
                game.__init__()
                # n_games+=1
                # agent.train_long_memory()
                
                if score > record:
                    record =score
                    # agent.model.save()
            
                print(' Scores ', score , ' Records: ',record)
                        
            # agent.k = []
            # plot_scores.append(score)
            # total_scores += score
            # mean_score = total_scores/agent.n_games
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores,plot_mean_scores)
              

if __name__ == '__main__':
    test()