# Patrons
import uuid

class n:
    ident = uuid.uuid1() # UUID might be a little overkill
    line  = bool() # 
    enter = int()
    cost  = 5 # An agent's associated cost for waiting in line
    beingServed = False
    order_complexity = 1.0 # Distributed between 1-2.5 that multiplies the order processing time
    def __init__(self,line,enter,cost) -> None:
        self.ident = uuid.uuid1()
        self.line = line
        self.enter = enter
        self.ext   = 0
        self.cost = cost
    def setBeingServed(self,b):
        self.beingServed = b

# Workers 
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

# Orders
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
realloc = boolean
"""
def occupy_Barista(n_i, K,time):
    b = False
    for k in K:
        if n_i.line == k.line and k.occupied == False:
            k.service_time.append(order(time,n_i))
            k.setOccupied(True)
            b = True
            break
    return b


"""
Generate Baristas one at a time
"""     
def genBaristas(div,num,i):
    if div * num <= i:
        return k(False,i)
    else:
        return k(True,i)

"""
Calculate the cost
"""
def cost_fun(K):
    sum = 0
    counter = 0
    # k.service_time[len(k.service_time)-2].ext+j.person.cost
    for i in K:
        calc_wait = 0
        for j in i.service_time:
            counter+=1
            if j.ext != 0:
                calc_wait+= (j.ext  - j.person.enter)
            else:
                calc_wait+= (i.service_time[len(i.service_time)-2].ext+ j.person.cost) - j.person.enter
        sum += calc_wait
        print(counter)
    return sum / counter

"""
Generate Patrons one at a time
"""     
def genPartrons(div,num,i,enter,cost):
     if div * num <= i:
        return n(False,enter,cost)
     else:
        return n(True,enter,cost)
"""
Free a bastista given that their time serving a person a function of enter time + cost is = curr time
"""
def freeBaristas(K,time,service_time):
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time)-1].start +  k.service_time[len(k.service_time)-1].person.cost  == time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time

"""
Simulation itself
"""
def simulation(K,rounds,div,stopGenAt,howMantToGenEachRound,cost):
    x = 0
    N = []
    realloc = False # TODO
    while x < rounds:
        x+=1
        service_time = 1
        if x % service_time == 0:
            freeBaristas(K,x,service_time)
        if x < stopGenAt:
            for i in range(howMantToGenEachRound):
                N.append(genPartrons(div,howMantToGenEachRound,i,x,cost))
        for n in N:
            if n.beingServed == False:
                if occupy_Barista(n,K,time=x):
                    n.setBeingServed(True)
     

def is_unfinished(j):
    if j.ext == 0:
        return True
    else:
        return False
    
def print_people(k):
    print("Barista {uuid} served: ".format(uuid = k.ident))
    i = 0
    for j in k.service_time:
            i+=1
            if is_unfinished(j) == False:
                print("customer {uuid} with enter: {enter} and exit {exit}".format(uuid = j.person.ident, enter = j.person.enter, exit = j.ext))
            else:
                print("customer {uuid} with enter: {enter} and exit {exit}".format(uuid = j.person.ident, enter = j.person.enter, exit = k.service_time[len(k.service_time)-2].ext+j.person.cost))


# At the end of all of the rounds       
def printBaristas(K):
    for k in K:
        print("Barista {uuid} served {patrons} with an average wait time of {wait}".format(uuid = k.ident, patrons = len(k.service_time),wait = cost_fun(K)))
        print_people(k)

       



def main():
   num_k = 4
   split = 0.5
   K = []
   for i in range(num_k):
      K.append(genBaristas(split,num_k,i))
   rounds = 10
   simulation(K,rounds,0.5,15,4,3)
   printBaristas(K)
   


if __name__ == "__main__":
    main()