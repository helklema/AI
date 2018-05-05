import gym
import numpy as np
import time
import os
from tqdm import tqdm

def sortFunc(el):
    return el[-1]

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

view = 0
agents = 100
trys = 100

env = gym.make("Taxi-v2")
n_actions = env.action_space.n
n_states = env.observation_space.n

policy  = [[1/n_actions for _ in range(n_actions)] for _ in range(n_states)]

observation = env.reset()

for t in tqdm(range(trys)):

    log = []
    rewards = []

    for agent in range(agents):
        tmp = []
        rewards = 0
        observation  = env.reset()
        while True:
            action = np.random.choice(n_actions, p = policy[observation])
            pair = [observation,action]
            observation, reward , done, info = env.step(action)
            if reward > -2: tmp.append(pair)
            if reward > 0: 
                for c in range(100): 
                    tmp.append(pair)
            rewards+=reward

            if done:
                if rewards >= -250: log.append([tmp,rewards])
                break
            

    log.sort(key = sortFunc)
    log.reverse()

    data = [[0,0,0,0,0,0] for _ in policy]
    for agentLog in log:
        for el in agentLog[0]:
            data[el[0]][el[1]]+=1
    for pos in range(len(data)):
        for p in range(n_actions):
            data[pos][p]+=1
    for pos in range(len(data)):
        s = sum(data[pos])
        for p in range(n_actions):
            data[pos][p]/=s
    policy=data[:]

rewards = 0
observation = env.reset()

r = []

for t in range(5):
    while True:   
        action = np.random.choice(n_actions, p = policy[observation]
        observation, reward , done, info = env.step(action)
        rewards+=reward
        print ('score: {}/ cost for current action {}'.format(rewards,reward))

        cls()
        env.render()
        time.sleep(0.01)

        if done:
            break

    r.append(rewards)
print (r)
