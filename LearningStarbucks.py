# Starbucks Problem with Reinforcement Learning
# We want to know what agents can do in real life if given opportunities to get through system of virtual and in-person queues.
# THIS DOES NOT WORK AT ALL. 
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint
from gym import Env
from gym.spaces import Box, Discrete
import random
import numpy as np


class n:
    ident = 1                  # UUID might be a little overkill
    line = bool()              # which line a patron is in
    enter = int()              # The Time at which the patron enters.
    cost = 5                   # An agent's associated cost for waiting in line
    beingServed = False        # Is a Patron being served
    alpha = 0.8                # is part of the virtual Queue only
    gamma = 1.2                # The Gamma component that makes an order more expensive by time
    hasExpensiveOrder = bool() # does Gamma come in account?

    def __init__(self, line, enter, cost, exp=False, gam=1) -> None:
        self.ident = 1
        self.line = line
        self.enter = enter
        self.ext = 0
        self.gamma = gam
        if exp:
            self.hasExpensiveOrder = True
            self.cost = cost * self.gamma
        else:
            self.cost = cost

    def setBeingServed(self, b):
        self.beingServed = b

    def is_being_served(self):
        return self.beingServed

    def setLine(self, l):
        self.line = l

    def hasExpensive(self):
        return self.hasExpensiveOrder

"""
Worker Class
"""

class k:
    indent = 1             # (Again) UUID may be a little overkill
    line = bool()         # True or false depending on which line a person is in
    occupied = bool()     # Is this barista currently serving anyone?
    # A list of the people a barista has served as an array of N patrons (n)
    service_time = []

    def __init__(self, line, i) -> None:
        self.ident = i
        self.line = line
        self.service_time = []
        self.occupied = False

    def setOccupied(self, b):
        self.occupied = b

class EspressoSim(Env):
    def __init__(self):
        self.action_space       = Discrete(3)
        self.observation_space  = Box(low=np.array([0]), high=np.array([100]))
        self.num_line_baristas  = 1
        self.num_queue_baristas = 1
        self.num_total_patrons  = 100
        self.num_line_patrons   = 50
        self.num_queue_patrons  = 50
        self.cost   = 3
        self.alpha  = 0.9
        self.rounds = 100
        
    
    def step(self, action):
        self.rounds -= 1 
        # Calculating the reward
        if (self.num_line_patrons * 3 / self.num_line_baristas)  == ((self.num_queue_patrons * self.alpha) / self.num_queue_baristas): 
            reward = 1
        elif (self.num_line_patrons * 3 / self.num_line_baristas) > ((self.num_queue_patrons * self.alpha) / self.num_queue_baristas): 
            reward = -1 
            self.num_queue_patrons += action
            self.num_line_patrons  -= action
        elif (self.num_line_patrons * 3 / self.num_line_baristas) < ((self.num_queue_patrons * self.alpha) / self.num_queue_baristas):
            reward = -1
            self.num_queue_patrons -= action
            self.num_line_patrons  += action
        # Checking if shower is done
        if self.rounds <= 0: 
            done = True
        else:
            done = False
        
        # Setting the placeholder for info
        info = {}
        # Returning the step information
        return self.state, reward, done, info
    def render(self):
        # This is where you would write the visualization code
        pass
    def reset(self):
        self.state = 38 + random.randint(-3,3)
        self.shower_length = 60 
        return self.state
    
env = EspressoSim()

episodes = 20 # 20 tries to get optimal amount of baristas
for episode in range(1, episodes+1):
    state = env.reset()
    done  = False
    score = 0 
    
    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score+=reward
    print('Episode:{} Score:{}'.format(episode, score))
print(env.num_line_patrons)
print(env.num_queue_patrons)