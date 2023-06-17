"""
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| This code contains the simulations (Random, Greedy, Greedy with Expensive Orders)
| Issue  |  Initials   |  Date       | Change
|   7    |    CJB      |  06/2023    | Initial Version 
|   8    |    CJB      |  06/2032    | Added Simulation that allows presetting each line
"""
import order
import patron as n
import random
import Sim_Costs as costs

"""
Free barista if they have finished with an order (does not take into account expensive orders)
"""
def freeBaristas(K, time)-> None:
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time)-1].start + k.service_time[len(k.service_time)-1].person.cost <= time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time

"""
Free barista if they have finished with an order in the case that there are expensive orders
"""
def freeBarista_with_gamma(K, time) -> None:
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time) - 1].start + k.service_time[len(k.service_time)-1].person.cost <= time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time

"""
Generate patrons to a random line
"""
def genPatronsRandom(div, num, i, enter, cost,queue_allowed) -> n:
    top = 10000
    if queue_allowed:
        rand = random.randint(0, top)
        if rand >= top * div:
            return n.patron(False, enter, cost)
        else:
            return n.patron(True, enter, cost)
    else:
        return n.patron(True,enter,cost)
    
"""
Checks if a list of patrons has an unserved member 
N        = list of patrons 
"""
def has_unserved_patron(N, K) -> bool:
    num_unserved = 0
    for x in N:
        if x.is_being_served() == False:
            num_unserved += 1
    for k in K:
        if len(k.service_time) > 2:
            if k.service_time[len(k.service_time)-1].ext == 0:
                return True
    if num_unserved > 0:
        return True
    else:
        return False

"""
n_i     = patron_i
K       = list of baristas
time    = clock time
"""

def occupy_Barista(n_i, K, time) -> bool:
    b = False
    for k in K:
        if n_i.line == k.line and k.occupied == False:
            k.service_time.append(order.order(time, n_i))
            k.setOccupied(True)
            b = True
            break
    return b

"""
Checks if a list of patrons has an unserved member 
N        = list of patrons 
"""

def has_unserved_patron(N, K) -> bool:
    num_unserved = 0
    for x in N:
        if x.is_being_served() == False:
            num_unserved += 1
    for k in K:
        if len(k.service_time) > 2:
            if k.service_time[len(k.service_time)-1].ext == 0:
                return True
    if num_unserved > 0:
        return True
    else:
        return False

"""
Is the line a barista is serving shorter than the other line? Then we allow reallocation, otherwise you cannot reallocate. 
"""


def allowed_to_reallocate(k, numLine, numQueue) -> bool:
    if k.line == True:
        if numLine == 0:
            return True
        else:
            return False
    else:
        if numQueue == 0:
            return True
        else:
            return False

"""
n_i     = patron_i
K       = list of baristas
time    = clock time
"""

def occupy_Barista_realloc(N, n_i, K, time) -> bool:
    b = False
    numLine = 0
    numQueue = 0
    for n in N:
        if n.beingServed == False:
            if n.line == True:
                numLine += 1
            else:
                numQueue += 1
    for k in K:
        if k.occupied == False and allowed_to_reallocate(k, numLine, numQueue):
            k.service_time.append(order.order(time, n_i))
            k.setOccupied(True)
            b = True
            break
    return b

"""
Simulation itself for random allocation that can be either line specific or reallocated based on who is openings and who arrives first 
K         = List of Baristas 
rounds    = Number of Rounds
div       = How to divide the later generated patrons
stopGenAt = When to stop generating people (This can be removed)
HMGER     = how many join simultaneously
cost      = complexity per order
realloc   = true or false to allow reallocation
"""

def Random_simulation(K, rounds, div, stopGenAt, howMantToGenEachRound, cost, realloc,queue_active,use_beta,beta) -> None:
    x = 0
    N = []
    if use_beta == True and queue_active == True:
        howMantToGenEachRound += beta
    if not realloc:
        while x <= rounds:
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(
                        div, howMantToGenEachRound, i, x, cost,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
    if realloc:
        while x < rounds:
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(
                        div, howMantToGenEachRound, i, x, cost,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x) == True:
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x) == True:
                        n.setBeingServed(True)

"""
allow a patron to select a line of their choice 
n_i     = patron_i
K       = list of baristas
time    = clock time
"""

def greedy_selection(K, N, enter, cost, alpha) -> bool:
    lineCost, queueCost = costs.cost_prior(K, N, enter, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True

"""
Takes care of each patrons line selection upon their entry
K       = List of Barista
enter   = clock time upon entry
cost    = cost per order for a patron (we set this to 3)
"""

def genGreedyPatrons(K, enter, cost, N, alpha,queue_allowed) -> n:
    if queue_allowed:
        selection = greedy_selection(K, N, enter, cost, alpha)
        return n.patron(selection, enter, cost)
    else:
        return n.patron(True,enter,cost)

"""
Simulation itself for greedy allocation without expensive orders
K            = List of Baristas 
rounds       = Number of Rounds
div          = How to divide the later generated patrons
stopGenAt    = When to stop generating people (This can be removed)
HMGER        = how many join simultaneously
cost         = complexity per order
realloc      = true or false to allow reallocation
alpha        = Convenience factor
queue_active = (Colloquially) Is GrubHub on or off?
use_beta     = Does Grubhub being on add additional orders to the system
beta         = What is the beta value (1 additional? 2 addition? 100 additional?) 
"""

def Greedy_Simulation(K,rounds, stopGenAt, howMantToGenEachRound, cost, realloc, alpha,queue_active,use_beta,beta,N = []) -> None:
    x = 0
    if use_beta ==  True and queue_active == True:
        howMantToGenEachRound += beta
    if not realloc:
        while x <= rounds:
            x += 1
            freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGreedyPatrons(K, x, cost, N, alpha,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
    if realloc:
        while x <= rounds:
            x += 1
            freeBaristas(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGreedyPatrons(K, x, cost, N, alpha,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=x):
                            n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            freeBaristas(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=x):
                            n.setBeingServed(True)

"""
Make a greedy selection in the case that the simulation contains expesive orders
"""
def greedy_selection_gamma(N, K, time, cost, alpha) -> bool:
    lineCost, queueCost = costs.cost_prior_Omni(N, K, time, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True

"""
Make a greedy selection in the case that the simulation contains expensiver orders (but the patrons don't take that into account)
"""
def myopic_greedy_selection_gamma(N, cost, alpha) -> bool:
    lineCost, queueCost = costs.cost_prior(N, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True
    
"""
Generate patrons that with some probability have expesive orders
"""
def genGammaPatrons(time, cost, N, K, alpha, gamma, useGamma, myopic, queue_active) -> n:
    if queue_active:
        if myopic == False:
            selection = greedy_selection_gamma(N, K, time, cost, alpha)
            return n.patron(selection, time, cost, exp=useGamma, gam=gamma)
        else:
            selection = myopic_greedy_selection_gamma(N, cost, alpha)
            return n.patron(selection, time, cost, exp=useGamma, gam=gamma)
    else:
        return n.patron(True,time,cost,exp=useGamma,gam=gamma)

"""
returns whether an order is expensive or not 
takes: probability of expensive
       number of simulation rounds
       how many are generated each round
       which gives a value between 0 and the total number of patrons
       if the number generated randomly is less than the probability of a patron having an expensive order times the total number of patrons the order is expensive 
       else the order is regular. 
       Example: 
            30% are expensive, 
            there are 50 rounds, 
            generating 2 per round. 
            This would mean if the random value falls less than 30 then the order is expensive, otherwise the order is normal. 
"""

def is_expensive(prob, rounds, howManyToGenEachRound, i) -> bool:
    total = rounds * howManyToGenEachRound
    r = random.randint(0, total)
    split = prob * total
    if r < split:
        return True
    else:
        return False


"""
Generate patrons to a random line
"""
def genPatron(Line,enter, cost) -> n:
    if Line == True:
        return n.patron(True, enter, cost)
    else:
        return n.patron(False, enter, cost)

"""
Create a simulation off a given starting point i.e. predefined number of people already in the system
same as greedy but takes a number of queue and line patrons to generate a ahead of each round
"""
def PresetSimulation(K,rounds,howManyToGenEachRound,cost,realloc,alpha,queue_active,use_beta,beta,num_q_patrons,num_l_patrons):
    queue_active = True # By Default
    N = []
    for i in range(0,num_l_patrons):
        N.append(genPatron(True,0,cost))
    for i in range(0,num_q_patrons):
        N.append(genPatron(False,0,cost))
    Greedy_Simulation(K,rounds,1000,howManyToGenEachRound,cost,realloc,alpha,queue_active,use_beta,beta,N)

"""
Ordering where expensive orders are taken into account by those entering the system
This takes into account the variable Gamma
Takes:
N     — a list of patrons
K     — a list of baristas
Time  — the current time
Cost  — Average cost for an order, kind of optional here because people have different order costs
Alpha — The Convenience Factor 
"""
def Gamma_Greedy_Simulation(K, rounds, stopGenAt, howMantToGenEachRound, cost, realloc, alpha, gamma, prob_expensive, myopic,queue_active,use_beta,beta) -> None:
    time = 0
    N = []
    if use_beta ==  True and queue_active == True:
        howMantToGenEachRound += beta
    if not realloc:
        while time <= rounds:
            time += 1
            freeBarista_with_gamma(K, time)
            if time < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGammaPatrons(time, cost, N, K, alpha, gamma, is_expensive(
                        prob_expensive, rounds, howMantToGenEachRound, i), myopic, queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time):
                        n.setBeingServed(True)
        while has_unserved_patron(N, K):
            time += 1
            freeBarista_with_gamma(K,time)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=time):
                        n.setBeingServed(True)
    if realloc:
        while time < rounds:
            time += 1
            service_time = 1
            if time % service_time == 0:
                freeBarista_with_gamma(K, time)
            if time < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGammaPatrons(time, cost, N, K, alpha, gamma, is_expensive(
                        prob_expensive, rounds, howMantToGenEachRound, i), myopic, queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=time):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=time):
                            n.setBeingServed(True)
        while has_unserved_patron(N, K):
            time += 1
            service_time = 1
            if time % service_time == 0:
                freeBarista_with_gamma(K, time)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=time):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=time):
                            n.setBeingServed(True)