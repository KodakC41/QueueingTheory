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
| Issue  |  Initials   |  Date       | Change
|   1    |    CJB      |  03/2023    | Initial Version: greedy and random simulations
|   2    |    CJB      |  05/2023    | Added Function to save baristas' patrons to a CSV for later use
|   3    |    CJB      |  06/2023    | Added Lambda and Gamma parameters and created new simulations to show their impacts. Beta was not added with this issue. 
|   6    |    CJB      |  06/2023    | Update Dyanmic cost fuction to give patrons more complete information, this also fixes bugs with reallocation costs as well. 
|        |             |             | Also added some arguments that will allow the simulation to be saved. 
"""

import uuid
import random
import argparse
import csv
import numpy

"""
Patron Class
"""


class n:
    ident = uuid.uuid1()       # UUID might be a little overkill
    line = bool()             # which line a patron is in
    enter = int()              # The Time at which the patron enters.
    cost = 5                  # An agent's associated cost for waiting in line
    beingServed = False        # Is a Patron being served
    alpha = 0.8                # is part of the virtual Queue only
    gamma = 1.2              # The Gamma component that makes an order more expensive by time
    hasExpensiveOrder = bool()  # does Gamma come in account?

    def __init__(self, line, enter, cost, exp=False, gam=1) -> None:
        self.ident = uuid.uuid1()
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
    indent = uuid.uuid1()  # (Again) UUID may be a little overkill
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


"""
Barista's Order Class
"""


class order:
    start = 0
    person = uuid.uuid4()
    ext = 0

    def __init__(self, start, person) -> None:
        self.person = person
        self.start = start


"""
n_i     = patron_i
K       = list of baristas
time    = clock time
"""


def occupy_Barista(n_i, K, time) -> bool:
    b = False
    for k in K:
        if n_i.line == k.line and k.occupied == False:
            k.service_time.append(order(time, n_i))
            k.setOccupied(True)
            b = True
            break
    return b


"""
Is the line a barista is serving shorter than the other line? Then we allow reallocation, otherwise you cannot reallocate. 
"""


def allowed_to_reallocate(k, numLine, numQueue):
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
            k.service_time.append(order(time, n_i))
            k.setOccupied(True)
            b = True
            break
    return b


# This is the cost function for reallocation, it requires a lot of book keeping.
def realloc_cost_fun(K, alpha):
    line_cost  = 0            # cost of a person who joined the line
    queue_cost = 0            # cost of a person who joined the queue
    l_counter  = 0            # number of people in each respective line
    q_counter  = 0            # number of people in each respective line
    total_served_q_b = 0      # total number queue barista served
    total_served_l_b = 0      # total number line  barista served
    total_q_b = total_l_b = 0 # number of baristas allocated to each line
    for k in K:
        if k.line == True:
            total_l_b += 1
        else:
            total_q_b += 1
        for j in k.service_time:
            if k.line == True:
                total_served_l_b += 1
            else:
                total_served_q_b += 1
            if j.person.line == True:
                if j.ext != 0:
                    l_counter += 1
                    line_cost += (j.ext - j.person.enter)
            else:
                if j.ext != 0:
                    q_counter += 1
                    queue_cost += ((j.ext - j.person.enter))
    return (line_cost / l_counter), ((queue_cost) / q_counter), l_counter, q_counter, total_served_l_b, total_served_q_b, total_l_b, total_q_b


"""
Calculate the cost after everyone has left the system (Posterior Cost)
K        = List of Barists 
"""


def cost_fun(K, cost, alpha) -> float:
    counter = 0
    calc_wait = 0
    if K.line:
        if len(K.service_time) < 1:
            return cost
        else:
            for j in K.service_time:
                counter += 1
                if j.ext != 0:
                    calc_wait += (j.ext - j.person.enter)
            return calc_wait / (counter)

    else:
        if len(K.service_time) <= 1:
            return cost * alpha
        else:
            for j in K.service_time:
                counter += 1
                if j.ext != 0:
                    calc_wait += (j.ext - j.person.enter)
            return (calc_wait / counter)


"""
Calculate the cost for a person entering a particular line based on those in line with them
N        = List of Customers 
"""


def cost_prior(K, N, time, cost, alpha) -> float:
    line_cost = 0
    queue_cost = 0
    for n in N:
        if n.beingServed == False:
            if n.line:
                line_cost += 1
            else:
                queue_cost += 1

    for k in K:
        if k.occupied:
            if len(k.service_time) > 1:
                if k.line:
                    serving_since = k.service_time[len(k.service_time)-1].start
                    if serving_since < time:
                        serving_until = serving_since + cost
                        line_cost += serving_until - serving_since
                else:
                    serving_since = k.service_time[len(k.service_time)-1].start
                    if serving_since < time:
                        serving_until = serving_since + cost
                        queue_cost += serving_until - serving_since
    line_cost = line_cost * cost
    queue_cost = queue_cost * (cost * alpha)
    return line_cost, queue_cost


"""
Omnicient Ordering where expensive orders are taken into account by those entering the system
This takes into account the variable Gamma
"""


def cost_prior_Omni(N, cost, alpha) -> float:
    line_cost = 0
    queue_cost = 0
    for n in N:
        if n.line:
            if n.beingServed == False:
                if n.hasExpensive():
                    line_cost += n.gamma
                else:
                    line_cost += 1
        else:
            if n.beingServed == False:
                if n.hasExpensive():
                    queue_cost += n.gamma
                else:
                    queue_cost += 1

    line_cost = line_cost * cost
    queue_cost = queue_cost * cost * alpha
    return line_cost, queue_cost


"""
Generate Patrons one at a time
div      = The number of baristas of a type to generate
num      = Current index of barista
i        = Max number to generate 
enter    = clock time enter
cost     = how complex is their order 
"""


def genPartrons(div, num, i, enter, cost) -> n:
    if div * num <= i:
        return n(False, enter, cost)
    else:
        return n(True, enter, cost)


"""
Takes care of each patrons line selection upon their entry
K       = List of Barista
enter   = clock time upon entry
cost    = cost per order for a patron (we set this to 3)
"""


def genGreedyPatrons(K, enter, cost, N, alpha,queue_allowed):
    if queue_allowed:
        selection = greedy_selection(K, N, enter, cost, alpha)
        return n(selection, enter, cost)
    else:
        return n(True,enter,cost)


def genPatronsRandom(div, num, i, enter, cost,queue_allowed) -> n:
    top = 10000
    if queue_allowed:
        rand = random.randint(0, top)
        if rand >= top * div:
            return n(False, enter, cost)
        else:
            return n(True, enter, cost)
    else:
        return n(True,enter,cost)


"""
Free a bastista given that their time serving a person a function of enter `time + cost is = curr time
K        = List of baristas 
time     = Clock time 
"""


def freeBaristas(K, time):
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time)-1].start + k.service_time[len(k.service_time)-1].person.cost <= time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time


def freeBarista_with_gamma(K, time):
    for k in K:
        if k.occupied == True and k.service_time[len(k.service_time) - 1].start + k.service_time[len(k.service_time)-1].person.cost <= time:
            k.setOccupied(False)
            k.service_time[len(k.service_time)-1].ext = time


"""
Checks if a list of patrons has an unserved member 
n        = list of patrons 
"""


def has_unserved_patron(N, K):
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


def has_unserved(k):
    for j in k:
        if k.ext == 0:
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


def Random_simulation(K, rounds, div, stopGenAt, howMantToGenEachRound, cost, realloc,queue_active,use_beta,beta) -> None:
    x = 0
    N = []
    if use_beta ==  True and queue_active == True:
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


def greedy_selection(K, N, enter, cost, alpha):
    lineCost, queueCost = cost_prior(K, N, enter, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True


"""
Each person looks at their cost for joining each line as a function of their order 
complexity and how many are in each line with a 50/50 split if a person joins the virtual queue they 
will incur a cost as a function of their alpha, otherwise they will just incur their pure cost as a function of nothing. 
"""


def Greedy_Simulation(K, rounds, stopGenAt, howMantToGenEachRound, cost, realloc, alpha,queue_active,use_beta,beta) -> None:
    x = 0
    N = []
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


def is_expensive(prob, rounds, howManyToGenEachRound, i):
    total = rounds * howManyToGenEachRound
    r = random.randint(0, total)
    split = prob * total
    if r < split:
        return True
    else:
        return False


def Omni_Gamma_Greedy_Simulation(K, rounds, stopGenAt, howMantToGenEachRound, cost, realloc, alpha, gamma, prob_expensive, myopic,queue_active,use_beta,beta) -> None:
    x = 0
    N = []
    if use_beta ==  True and queue_active == True:
        howMantToGenEachRound += beta
    if not realloc:
        while x <= rounds:
            x += 1
            freeBarista_with_gamma(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGammaPatrons(x, cost, N, alpha, gamma, is_expensive(
                        prob_expensive, rounds, howMantToGenEachRound, i), myopic,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            freeBarista_with_gamma(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista(n, K, time=x):
                        n.setBeingServed(True)
    if realloc:
        while x < rounds:
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBarista_with_gamma(K, x)
            if x < stopGenAt:
                for i in range(howMantToGenEachRound):
                    N.append(genGammaPatrons(x, cost, N, alpha, gamma, is_expensive(
                        prob_expensive, rounds, howMantToGenEachRound, i), myopic,queue_active))
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=x):
                            n.setBeingServed(True)
        while has_unserved_patron(N, K):
            x += 1
            service_time = 1
            if x % service_time == 0:
                freeBarista_with_gamma(K, x)
            for n in N:
                if n.beingServed == False:
                    if occupy_Barista_realloc(N, n, K, time=x):
                        n.setBeingServed(True)
                    else:
                        if occupy_Barista(n, K, time=x):
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
Saves a list of baristas and those they have served to a CSV file 
"""


def print_people(K, file_name="customers_served") -> None:
    i = 0
    with open('{file_name}.csv'.format(file_name=file_name), 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Barista", "Patron", "Enter",
                 "Cost", "Exit", "Line", "Final Cost"]
        writer.writerow(field)
        for k in K:
            for j in k.service_time:
                i += 1
                if is_unfinished(j) == False:
                    if j.person.line:
                        ext = j.ext - j.person.enter
                        writer.writerow(
                            [k.ident, i, j.person.enter, j.person.cost, j.ext, "line", ext])
                    else:
                        ext = j.ext - j.person.enter
                        writer.writerow(
                            [k.ident, i, j.person.enter, j.person.cost, j.ext, "queue", ext])


"""
Prints the used baristas and the average cost incurred by the patrons in their lines
- Optional function to save the baristas and those they have served to a .csv file. 
"""


def printBaristas(K, p, cost, alpha, reallocation, file_name,use_queue) -> None:
    if reallocation != True:
        queueWait       = lineWait          = 0 # For Calculating the average wait time
        numQueue        = numLine           = 0 # For Calculating the number in each line
        numExpensiveQ   = numExpensiveL     = 0 # For Calculating the number of expensive orders in each line
        numQueueBaristas = numLineBaristas  = 0 # For Calculating the number of baristas in each line
        if use_queue == True:
            for k in K:
                if k.line == True:
                    numLineBaristas += 1
                    lineWait += cost_fun(k, cost, alpha)
                    numLine += int(len(k.service_time))
                    numExpensiveL += countExpensive(k)
                else:
                    numQueueBaristas +=1
                    queueWait += cost_fun(k, cost, alpha)
                    numQueue += int(len(k.service_time))
                    numExpensiveQ += countExpensive(k)
            print("Line Baristas served {patrons} with an average cost of {wait}".format(
                patrons=numLine, wait=round(lineWait)/numLineBaristas))
            print("Queue Baristas served {patrons} with an average perceived cost of {wait} and with an average time cost of {actual}".format(
                patrons=numQueue, wait=round((queueWait * alpha) / numQueueBaristas), actual=round(queueWait)/numQueueBaristas))
            print("The line barista(s) served {l} complex orders and the queue barista(s) served {q}".format(
                l=numExpensiveL, q=numExpensiveQ))
            if p:
                print_people(K, file_name)
        else:
            lineWait          = 0 # For Calculating the average wait time
            numLine           = 0 # For Calculating the number in each line
            numExpensiveL     = 0 # For Calculating the number of expensive orders in each line
            numLineBaristas   = 0 # For Calculating the number of baristas in each line
            for k in K:
                numLineBaristas += 1
                lineWait += cost_fun(k, cost, alpha)
                numLine += int(len(k.service_time))
                numExpensiveL += countExpensive(k)
            print("Line Baristas served {patrons} with an average cost of {wait}".format(
                patrons=numLine, wait=round(lineWait)/numLineBaristas))
    else:
        if use_queue == True:
            lineWait, queueWait, numLine, numQueue, servedLine, servedQueue,numLineBaristas,numQueueBaristas = realloc_cost_fun(
                K, alpha)
            print("Line held {patrons} with an average cost of {wait} and the line barista made {served} orders in that time".format(
                patrons=numLine, wait=round(lineWait), served=servedLine))
            print("Queue held {patrons} with an average cost of {wait} and the queue barista made {served} orders in that time".format(
                patrons=numQueue, wait=round((queueWait * alpha)), served=servedQueue))
            if p:
                print_people(K, file_name)
        else:
            lineWait          = 0 # For Calculating the average wait time
            numLine           = 0 # For Calculating the number in each line
            numExpensiveL     = 0 # For Calculating the number of expensive orders in each line
            numLineBaristas   = 0 # For Calculating the number of baristas in each line
            for k in K:
                numLineBaristas += 1
                lineWait += cost_fun(k, cost, alpha)
                numLine += int(len(k.service_time))
                numExpensiveL += countExpensive(k)
            print("Line Baristas served {patrons} with an average cost of {wait}".format(
                patrons=numLine, wait=round(lineWait)/numLineBaristas))





def countExpensive(k):
    countE = 0
    for j in k.service_time:
        if j.person.hasExpensive():
            countE += 1
    return countE


"""
Generate Baristas one at a time
div      = The number of baristas of a type to generate
num      = Current index of barista
i        = Max number to generate 
"""


def genBaristas(div, maxi, i, queue_active):
    if queue_active == True:
        if i < (maxi * div):
            return k(False, i)
        elif i >= div:
            return k(True, i)
    else:
        return k(True,i)


def greedy_selection_gamma(N, cost, alpha):
    lineCost, queueCost = cost_prior_Omni(N, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True


def myopic_greedy_selection_gamma(N, cost, alpha):
    lineCost, queueCost = cost_prior(N, cost, alpha)
    if lineCost > queueCost:
        return False
    else:
        return True


def genGammaPatrons(enter, cost, N, alpha, gamma, useGamma, myopic,queue_active):
    if queue_active:
        if myopic == False:
            selection = greedy_selection_gamma(N, cost, alpha)
            return n(selection, enter, cost, exp=useGamma, gam=gamma)
        else:
            selection = myopic_greedy_selection_gamma(N, cost, alpha)
            return n(selection, enter, cost, exp=useGamma, gam=gamma)
    else:
        return n(True,enter,cost,exp=useGamma,gam=gamma)


"""
Hire (Generate) Instances of baristas (k)
"""


def HumanResources(num_k, div,queue_active):
    K = []
    for i in range(num_k):
        K.append(genBaristas(div, num_k, i,queue_active))
    return K


def main():
    # This looks terrible to look at, but it's all there. 
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--baristanum",
                         help="Number of Baristas",  type=int, default=2)
    parser.add_argument("-n", "--customernum",
                         help="Number of Customers", type=int, default=2)
    parser.add_argument(
        "-r", "--rounds",help="Number of Rounds",    type=int, default=200)
    parser.add_argument("-s", "--split", help="Split", type=float, default=0.5)
    parser.add_argument('--reallocation',             action=argparse.BooleanOptionalAction,
                        default=False, help="Allow Reallocation?")
    parser.add_argument(
        "-a", "--alpha", help="Alpha (conviniece value)", type=float, default=0.8)
    parser.add_argument(
        "-c", "--cost",  help="Cost per order", type=int, default=3)
    parser.add_argument(
        "-b", "--beta",  help="How many to add to the system (Beta)", type=int, default=1)
    parser.add_argument(
        "-g", "--gamma", help="How expensive is an expensiver order (Gamma)", type=float, default=1.1)
    parser.add_argument(
        "-l", "--lam",   help="What is the liklihood of a person having an expensive order", type=float, default=0.2)
    parser.add_argument("-filename", "--file_path", help="Where shoudld the output file be saved?",
                        type=str, default="customers_served")  # TODO Make this work
    parser.add_argument("-save_sim", "--save_sim", help="Should the simulation be saved to an output file?",
                        action=argparse.BooleanOptionalAction, default=False)  # TODO Make this work

    # What type of simulation should be run?
    parser.add_argument('--use_gamma',             action=argparse.BooleanOptionalAction,
                        default=False, help="Use Gamma or not")
    parser.add_argument('--myopic',                action=argparse.BooleanOptionalAction,
                        default=False, help="Are Patrons Myopic or not?")
    parser.add_argument('--both',                  action=argparse.BooleanOptionalAction,
                        default=False, help="Run both Greedy case that use gamma or not")
    parser.add_argument('--all',                   action=argparse.BooleanOptionalAction,
                        default=False, help="Run all Simulations")  # Run with Gamma, random, and without Gamma
    parser.add_argument("--random",                action=argparse.BooleanOptionalAction,
                        default=False, help="Run the random simulation")
    parser.add_argument('-use_queue','--queue_active',help="Is GrubHub on or Off",action=argparse.BooleanOptionalAction,default=False)
    parser.add_argument('-use_beta', '--beta_active', help="Use Beta or not?",    action=argparse.BooleanOptionalAction,default=False)
    args = parser.parse_args()

    # All the key variables for the simulations
    num_k     = args.baristanum       # Works
    split     = args.split            # Works 
    custNum   = args.customernum      # Works
    rounds    = args.rounds           # Works
    realloc   = args.reallocation     # Works
    cost      = args.cost             # Works
    alpha     = args.alpha            # Works
    beta      = args.beta             # TODO BETA in progress
    use_beta  = args.beta_active      # TODO Part of BETA 
    gamma     = args.gamma            # Works
    myopic    = args.myopic           # Works
    lam       = args.lam              # Works 
    withGamma = args.use_gamma        # Works
    Both      = args.both             # Works
    All       = args.all              # Works
    rand      = args.random           # Works
    save_sim  = args.save_sim         # Works
    file_name = args.file_path        # Works
    use_queue = args.queue_active     # Should work...

    if withGamma == True and not Both and not All and not rand:
        print("—>Greedy Simulation")
        K = HumanResources(num_k,split,use_queue)
        Omni_Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif withGamma == False and not Both and not All and not rand:  # Default
        print("—>Greedy Simulation")
        K = HumanResources(num_k,split,use_queue)
        Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif Both and not All and not rand:
        print("—>Greedy Simulation without Gamma")
        K = HumanResources(num_k,split,use_queue)
        Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print("—>Greedy Simulation with Gamma")
        K = HumanResources(num_k,split,use_queue)
        Omni_Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif All == True:
        print("->Random Simulation")
        K = HumanResources(num_k,split,use_queue)
        Random_simulation(K, rounds, 0.5, 1000, custNum, cost, realloc,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print()
        print("—>Greedy Simulation without Gamma")
        K = HumanResources(num_k,split,use_queue)
        Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print()
        print("—>Greedy Simulation with Gamma")
        K = HumanResources(num_k,split,use_queue)
        Omni_Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif rand:
        print("->Random Simulation")
        K = HumanResources(num_k,split,use_queue)
        Random_simulation(K, rounds, 0.5, 1000, custNum, cost, realloc,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)


if __name__ == "__main__":
    main()
