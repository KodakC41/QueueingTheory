# Patrons
import uuid
import random
import argparse

"""
The alpha used if a person has had their drink made by a barista in the virtual queue. 
"""
ALPHA = 0.8
COST  = 3


"""
Patron Class
"""
class n:
    ident = uuid.uuid1() # UUID might be a little overkill
    line  = bool() # 
    enter = int()
    cost  = 5 # An agent's associated cost for waiting in line
    beingServed = False
    alpha = 0.8 # is part of the virtual Queue only
    def __init__(self,line,enter,cost) -> None:
        self.ident = uuid.uuid1()
        self.line = line
        self.enter = enter
        self.ext   = 0
        self.cost = cost
    def setBeingServed(self,b):
        self.beingServed = b
    def is_being_served(self):
        return self.beingServed
    def setLine(self,l):
        self.line= l


"""
Worker Class
""" 
class k:
    indent = uuid.uuid1()
    line = bool()
    occupied = bool()
    service_time = []
    def __init__(self,line,i) -> None:
        self.ident = i
        self.line = line
        self.service_time = []
        self.occupied = False

    def setOccupied(self,b):
        self.occupied = b

"""
Barista's Order Class
"""
class order:
    start  = 0
    person = uuid.uuid4()
    ext    = 0
    
    def __init__(self,start,person) -> None:
        self.person = person
        self.start = start


"""
n_i     = patron_i
K       = list of baristas
time    = clock time
"""
def occupy_Barista(n_i, K,time) -> bool:
    b = False
    for k in K:
        if n_i.line == k.line and k.occupied == False:
            k.service_time.append(order(time,n_i))
            k.setOccupied(True)
            b = True
            break
    return b

"""
n_i     = patron_i
K       = list of baristas
time    = clock time
"""
def occupy_Barista_realloc(n_i, K,time) -> bool:
    b = False
    for k in K:
        if k.occupied == False:
            k.service_time.append(order(time,n_i))
            k.setOccupied(True)
            b = True
            break
    return b


"""
Generate Baristas one at a time
div      = The number of baristas of a type to generate
num      = Current index of barista
i        = Max number to generate 
"""     
def genBaristas(div,num,i):
    if div * num <= i:
        return k(False,i)
    else:
        return k(True,i)


"""
Calculate the cost after everyone has left the system (Posterior Cost)
K        = List of Barists 
"""
def cost_fun(K) -> float:
    counter = 0
    calc_wait = 0
    if K.line:
        if len(K.service_time) < 1:
            return COST
        else:
            for j in K.service_time:
                counter+=1
                if j.ext != 0:
                    calc_wait+= (j.ext  - j.person.enter) 
            return calc_wait / (counter)
      
    else:
        if len(K.service_time) <= 1:
            return COST * ALPHA
        else:
            for j in K.service_time:
                counter+=1
                if j.ext != 0:
                    calc_wait+= (j.ext  - j.person.enter)
            return (calc_wait / counter) * ALPHA
        
"""
Calculate the cost for a person entering a particular line based on those in line with them
N        = List of Customers 
"""
def cost_prior(N) -> float:
    line_cost  = 0
    queue_cost = 0
    for n in N:
        if n.line:
            line_cost+=1
        else:
            queue_cost+=1
    line_cost = line_cost * COST
    queue_cost = queue_cost * (COST * ALPHA)
    return line_cost,queue_cost
    
"""
Calculate the cost but without alpha because each patron has already greedily measured cost by their alpha
K        = List of Barists 
"""
def cost_fun_greedy(K) -> float:
    counter = 0
    calc_wait = 0
    for j in K.service_time:
        counter+=1
        if j.ext != 0:
                calc_wait+= (j.ext  - j.person.enter) 
    return calc_wait / counter


"""
Generate Patrons one at a time
div      = The number of baristas of a type to generate
num      = Current index of barista
i        = Max number to generate 
enter    = clock time enter
cost     = how complex is their order 
"""     
def genPartrons(div,num,i,enter,cost) -> n:
     if div * num <= i:
        return n(False,enter,cost)
     else:
        return n(True,enter,cost)
     
"""
Takes care of each patrons line selection upon their entry
K       = List of Barista
enter   = clock time upon entry
cost    = cost per order for a patron (we set this to 3)
"""
def genGreedyPatrons(enter,cost,K,N):
    selection  = greedy_selection(N)
    return n(selection,enter,cost)


def genPatronsRandom(div,num,i,enter,cost) -> n:
    top = 10000
    rand = random.randint(0,top)
    if rand >= top * div:
        return n(False,enter,cost)
    else:
        return n(True,enter,cost)


"""
Free a bastista given that their time serving a person a function of enter `time + cost is = curr time
K        = List of baristas 
time     = Clock time 
"""
def freeBaristas(K,time,service_time):
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time)-1].start +  k.service_time[len(k.service_time)-1].person.cost  == time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time

"""
Checks if a list of patrons has an unserved member 
n        = list of patrons 
"""
def has_unserved_patron(n):
    num_unserved = 0
    for x in n:
        if x.is_being_served() == False:
            num_unserved+=1
    if num_unserved > 0:
        return True
    else:
        return False

"""
Simulation itself for random allocation that can be either line specific or reallocated based on who is openings and who arrives first 
K         = List of Barista
rounds    = Number of Rounds
div       = how to divide the later generated patrons
stopGenAt = when to stop generating people 
HMGER     = how many join simultaneously
cost      = complexity per order
realloc   = true or false to allow reallocation
"""
def Random_simulation(K,rounds,div,stopGenAt,howMantToGenEachRound,cost,realloc) -> None:
    x = 0
    N = [] 
    if not realloc:
        while x <= rounds:
            x+=1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K,x,service_time)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(div,howMantToGenEachRound,i,x,cost))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n,K,time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x+=1
            service_time = 1
            if x % service_time == 0:
                    freeBaristas(K,x,service_time)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n,K,time=x):
                        n.setBeingServed(True)
    if realloc:
        while x < rounds:
            x+=1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K,x,service_time)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genPatronsRandom(div,howMantToGenEachRound,i,x,cost))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(n,K,time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x+=1
            service_time = 1
            if x % service_time == 0:
                    freeBaristas(K,x,service_time)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(n,K,time=x):
                        n.setBeingServed(True)
        
"""
allow a patron to select a line of their choice 
n_i     = patron_i
K       = list of baristas
time    = clock time
"""
def greedy_selection(N):
    lineCost,queueCost = cost_prior(N)
    if lineCost > queueCost:
        return False
    else:
        return True


        


"""
Each person looks at their cost for joining each line as a function of their order 
complexity and how many are in each line with a 50/50 split if a person joins the virtual queue they 
will incur a cost as a function of their alpha, otherwise they will just incur their pure cost as a function of nothing. 
"""
def Greedy_Simulation(K,rounds,stopGenAt,howMantToGenEachRound,cost,realloc) -> None:
    x = 0
    N = [] 
    if not realloc:
        while x <= rounds:
            x+=1
            freeBaristas(K,x,1)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGreedyPatrons(x,cost,K,N))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n,K,time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x+=1
            freeBaristas(K,x,1)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n,K,time=x):
                        n.setBeingServed(True)
    if realloc:
        while x < rounds:
            x+=1
            service_time = 1
            if x % service_time == 0:
                freeBaristas(K,x,1)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGreedyPatrons(x,cost,K,N))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(n,K,time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N):
            x+=1
            service_time = 1
            if x % service_time == 0:
                    freeBaristas(K,x,1)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(n,K,time=x):
                        n.setBeingServed(True)


"""
Has a patron had their drink finished?
"""
def is_unfinished(j) -> bool:
    if j.ext == 0:
        return True
    else:
        return False

"""
Print the people that have been helped by a certain barista... use at your own risk.
"""
def print_people(k) -> None:
    print("Barista {uuid} served: ".format(uuid = k.ident + 1))
    i = 0
    for j in k.service_time:
            i+=1
            if is_unfinished(j) == False:
                if j.person.line:
                    print("customer {uuid} with enter: {enter} and exit  {exit} from line {line}".format(uuid = i, enter = j.person.enter, exit = j.ext,line='l'))
                else:
                    print("customer {uuid} with enter: {enter} and exit  {exit} from line {line}".format(uuid = i, enter = j.person.enter, exit = j.ext,line='q') )

def printBaristas(K,p,greedy) -> None:
    queueWait = 0
    lineWait  = 0
    numQueue  = 0
    numLine   = 0
    for k in K:
        if not greedy:
            if k.line:
                lineWait += cost_fun(k)
                numLine  += len(k.service_time)
            else:
                queueWait += cost_fun(k)
                numQueue  += len(k.service_time)
        else:
            if k.line:
                lineWait += cost_fun(k)
                numLine += int(len(k.service_time))
            else:
                queueWait += cost_fun(k)
                numQueue += int(len(k.service_time) - 1) 
    print("Line Baristas served {patrons} with an average cost of {wait}".format(patrons = numLine,wait = lineWait / 2))
    print("Queue Baristas served {patrons} with an average cost of {wait}".format(patrons = numQueue,wait = (queueWait / 2) * 0.8))


"""
Hire (Generate) Instances of baristas (k)
"""
def HumanResources(num_k,split):
    K = []
    for i in range(num_k):
      K.append(genBaristas(split,num_k,i))
    return K



def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("-k", "--baristanum", help="Number of Baristas",type=int,default=2)
   parser.add_argument("-n", "--customernum", help="Number of Customers",type=int,default=2)
   parser.add_argument("-r", "--rounds", help="Number of Rounds", type=int,default=200)
   parser.add_argument("-s","--split",help="Split",type=float,default=0.5)
   parser.add_argument("-alloc","--reallocation",help="Allow Reallocation?",type=bool,default=False)
   args = parser.parse_args()
   num_k = args.baristanum
   split = args.split
   custNum = args.customernum
   K = HumanResources(num_k=num_k,split=split)
   rounds = args.rounds
   realloc = args.reallocation
   print()
   print("—>Random Simulation")
#    Random_simulation(K,rounds,0.5,200,2,3,False)
#    printBaristas(K,False,False)
   print()
   print("—>Greedy Simulation")
   K = HumanResources(num_k=num_k,split=split)
   Greedy_Simulation(K,rounds,1000,custNum,COST,realloc)
   printBaristas(K,False,True)


if __name__ == "__main__":
    main()