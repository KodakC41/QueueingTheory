"""
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| This code demonstrates a cutomer's best payoff based on their percieved conviniece for a virtual queue against
| the number of baristas to serve them and the cost of their order. 
| most variables are adjustable including:
| - alpha,
| - cost,
| - number of baristas, 
| - number of patrons, 
| - how many to serve virtual line vs. in person, 
| - how many simulation rounds, 
| - reallocation (T/F)
| Change Log:
|_Issue__|__Initials___|__Date_______|__Change_______
|   1         CJB      |  03/2023    | Initial Version: greedy and random simulations
"""

# This code demonstrates that for some values of alpha where one over estimate the convience value 
# of using mobile ordering their payoff can be worse than if they were to just get in line
# This shows that for some percieved values of conviniences there need to be proportionally more baristas to 
# serve a line with such a percieved value of convinience. 

import uuid
import random
import argparse
import csv

"""
Patron Class
"""
class n:
    ident = uuid.uuid1() # UUID might be a little overkill
    line  = bool()       # which line a patron is in
    enter = int()        # The Time at which the patron enters. 
    cost  = 5            # An agent's associated cost for waiting in line
    beingServed = False  # Is a Patron being served
    alpha = 0.8          # is part of the virtual Queue only
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
    indent = uuid.uuid1() # (Again) UUID may be a little overkill
    line = bool()         # True or false depending on which line a person is in
    occupied = bool()     # Is this barista currently serving anyone?
    service_time = []     # A list of the people a barista has served as an array of N patrons (n)
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
Calculate the cost after everyone has left the system (Posterior Cost)
K        = List of Barists 
"""
def cost_fun(K,cost,alpha) -> float:
    counter = 0
    calc_wait = 0
    if K.line:
        if len(K.service_time) < 1:
            return cost
        else:
            for j in K.service_time:
                counter+=1
                if j.ext != 0:
                    calc_wait+= (j.ext  - j.person.enter) 
            return calc_wait / (counter)
      
    else:
        if len(K.service_time) <= 1:
            return cost * alpha
        else:
            for j in K.service_time:
                counter+=1
                if j.ext != 0:
                    calc_wait+= (j.ext  - j.person.enter)
            return (calc_wait / counter) * alpha
        
"""
Calculate the cost for a person entering a particular line based on those in line with them
N        = List of Customers 
"""
def cost_prior(N,cost,alpha) -> float:
    line_cost  = 0
    queue_cost = 0
    for n in N:
        if n.line:
            line_cost+=1
        else:
            queue_cost+=1
    line_cost = line_cost * cost
    queue_cost = queue_cost * (cost * alpha)
    return line_cost,queue_cost
    

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
def genGreedyPatrons(enter,cost,N,alpha):
    selection  = greedy_selection(N,cost,alpha)
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
def greedy_selection(N,cost,alpha):
    lineCost,queueCost = cost_prior(N,cost,alpha)
    if lineCost > queueCost:
        return False
    else:
        return True


"""
Each person looks at their cost for joining each line as a function of their order 
complexity and how many are in each line with a 50/50 split if a person joins the virtual queue they 
will incur a cost as a function of their alpha, otherwise they will just incur their pure cost as a function of nothing. 
"""
def Greedy_Simulation(K,rounds,stopGenAt,howMantToGenEachRound,cost,realloc,alpha) -> None:
    x = 0
    N = [] 
    if not realloc:
        while x <= rounds:
            x+=1
            freeBaristas(K,x,1)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGreedyPatrons(x,cost,N,alpha))
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
TODO: Update to save as CSV: Print the people that have been helped by a certain barista... use at your own risk. 
"""
def print_people(K) -> None:
    # print("Barista {uuid} served: ".format(uuid = k.ident + 1))
    i = 0
    
    with open('customers_served.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Barista","Patron","Enter", "Exit","Line"]
        writer.writerow(field)
        for k in K:
            for j in k.service_time:
                i+=1
                if is_unfinished(j) == False:
                    if j.person.line:
                        writer.writerow([k.ident,i,j.person.enter,j.ext,"1"])
                        # print("customer {uuid} with enter: {enter} and exit  {exit} from line {line}".format(uuid = i, enter = j.person.enter, exit = j.ext,line='l'))
                    else:
                        # print("customer {uuid} with enter: {enter} and exit  {exit} from line {line}".format(uuid = i, enter = j.person.enter, exit = j.ext,line='q') )
                        writer.writerow([k.ident,i,j.person.enter,j.ext,"0"])
        
    

def printBaristas(K,p,greedy,cost,alpha) -> None:
    queueWait = 0
    lineWait  = 0
    numQueue  = 0
    numLine   = 0
    for k in K:
        if not greedy:
            if k.line:
                lineWait += cost_fun(k,cost,alpha)
                numLine  += len(k.service_time)
            else:
                queueWait += cost_fun(k,cost,alpha)
                numQueue  += len(k.service_time)
        else:
            if k.line:
                lineWait += cost_fun(k,cost,alpha)
                numLine += int(len(k.service_time))
            else:
                queueWait += cost_fun(k,cost,alpha)
                numQueue += int(len(k.service_time) - 1) 
    print("Line Baristas served {patrons} with an average cost of {wait}".format(patrons = numLine,wait = round(lineWait / 2)))
    print("Queue Baristas served {patrons} with an average cost of {wait}".format(patrons = numQueue,wait = round((queueWait / 2) * 0.8)))
    if p:
        print_people(K)

"""
Generate Baristas one at a time
div      = The number of baristas of a type to generate
num      = Current index of barista
i        = Max number to generate 
"""     
def genBaristas(div,maxi,i):
    if i < div:
        return k(False,i)
    elif i >= div and i <= maxi:
        return k(True,i)


"""
Hire (Generate) Instances of baristas (k)
"""
def HumanResources(num_k,div):
    K = []
    for i in range(num_k):
      K.append(genBaristas(div,num_k,i))
    return K


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument("-k", "--baristanum", help="Number of Baristas",type=int,default=2)
   parser.add_argument("-n", "--customernum", help="Number of Customers",type=int,default=2)
   parser.add_argument("-r", "--rounds", help="Number of Rounds", type=int,default=200)
   parser.add_argument("-s","--split",help="Split",type=float,default=1)
   parser.add_argument("-alloc","--reallocation",help="Allow Reallocation?",type=bool,default=False)
   parser.add_argument("-a","--alpha",help="Alpha (conviniece value)",type=float,default=0.8)
   parser.add_argument("-c","--cost",help="Cost per order",type=int,default=3)
   args    = parser.parse_args()
   num_k   = args.baristanum
   split   = args.split
   custNum = args.customernum
   rounds  = args.rounds
   realloc = args.reallocation
   cost    = args.cost
   alpha   = args.alpha 
   K = HumanResources(num_k=num_k,div=split)
   print()
   print("—>Random Simulation")
   Random_simulation(K,rounds,0.6,200,2,3,False)
   printBaristas(K,False,False,cost,alpha)
   print()
   print("—>Greedy Simulation")
   K = HumanResources(num_k=num_k,div=split)
   Greedy_Simulation(K,rounds,1000,custNum,cost,realloc,alpha)
   printBaristas(K,False,True,cost,alpha)


if __name__ == "__main__":
    main()