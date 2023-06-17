"""
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| This code contains the methods for calculating cost
| Issue  |  Initials   |  Date       | Change
|   7    |    CJB      |  06/2023    | Initial Version 
"""

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
        
# This is the cost function for reallocation, it requires a lot of book keeping.
def realloc_cost_fun(K):
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
    line_cost = line_cost * cost
    queue_cost = queue_cost * (cost * alpha)
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
    return line_cost, queue_cost

"""
Omnicient Ordering where expensive orders are taken into account by those entering the system
This takes into account the variable Gamma
Takes:
N     — a list of patrons
K     — a list of baristas
Time  — the current time
Cost  — Average cost for an order, kind of optional here because people have different order costs
Alpha — The Convenience Factor 
"""
def cost_prior_Omni(N, K, time, cost, alpha) -> float:
    line_cost = 0
    queue_cost = 0
    for n in N:
        if n.beingServed == False:
            if n.line:
                if n.hasExpensive():
                    line_cost += n.gamma
                else:
                    line_cost += 1
            else:
                if n.hasExpensive():
                    queue_cost += 1
                else:
                    queue_cost +=1
    line_cost = line_cost * cost
    queue_cost = queue_cost * (cost * alpha)
    for k in K:
        if k.occupied:
            # We only want to do this it is not the first patron served
            if len(k.service_time) > 1:
                if k.line == True:
                    being_served = k.service_time[len(k.service_time)-1] # Store the last person in each barista's service line
                    # The start time of the patron being served
                    serving_since = being_served.start
                    if serving_since < time:
                        if being_served.person.hasExpensive():
                            serving_until = serving_since + n.gamma
                            line_cost += serving_until - serving_since
                        else:
                            serving_until = serving_since + cost
                            line_cost += serving_until - serving_since
                else:
                    being_served = k.service_time[len(k.service_time)-1] # Store the last person in each barista's service line
                    serving_since = being_served.start
                    if serving_since < time:
                        if being_served.person.hasExpensive():
                            serving_until = serving_since + n.gamma
                            queue_cost += serving_until - serving_since
                        else:
                            serving_until = serving_since + cost
                            queue_cost += serving_until - serving_since
    return line_cost, queue_cost