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
|   7    |    CJB      |  06/2023    | Added Beta and change print functions. In addition, new files were created for better code design. 
|   8    |    CJB      |  06/2023    | Update for present simulations
"""

import argparse
import csv
import Simulations as sim
import Sim_Costs as costs

# Now in separate files for better code chunking 
import barista



def is_unfinished(j) -> bool:
    if j.ext == 0:
        return True
    else:
        return False

"""
Saves a list of baristas and those they have served to a CSV file 
Takes:
K         = list of baristas
file_name = where do we save it? defaults to customers_served.csv
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
Prints the simulation in the case where GrubHub is off — 
"""
def print_line_only(K,p,cost,alpha,file_name) -> None:
    lineWait          = 0 # For Calculating the average wait time
    numLine           = 0 # For Calculating the number in each line
    numExpensiveL     = 0 # For Calculating the number of expensive orders in each line
    numLineBaristas   = 0 # For Calculating the number of baristas in each line
    for k in K:
        numLineBaristas += 1
        lineWait += costs.cost_fun(k, cost, alpha)
        numLine += int(len(k.service_time))
        numExpensiveL += countExpensive(k)
    print("Line Baristas served {patrons} with an average cost of {wait}".format(
        patrons=numLine, wait=round(lineWait)/numLineBaristas))
    if p:
        print_people(K, file_name)

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
                    lineWait += costs.cost_fun(k, cost, alpha)
                    numLine += int(len(k.service_time))
                    numExpensiveL += countExpensive(k)
                else:
                    numQueueBaristas +=1
                    queueWait += costs.cost_fun(k, cost, alpha)
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
            print_line_only(K,p,cost,alpha,file_name)
    else:
        if use_queue == True:
            lineWait, queueWait, numLine, numQueue, servedLine, servedQueue,numLineBaristas,numQueueBaristas = costs.realloc_cost_fun(
                K)
            print("Line held {patrons} with an average cost of {wait} and the line barista made {served} orders in that time".format(
                patrons=numLine, wait=round(lineWait), served=servedLine))
            print("Queue held {patrons} with an average cost of {wait} and the queue barista made {served} orders in that time".format(
                patrons=numQueue, wait=round((queueWait * alpha)), served=servedQueue))
            if p:
                print_people(K, file_name)
        else:
            print_line_only(K,p,cost,alpha,file_name)
            

def countExpensive(k) -> int:
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


def genBaristas(div, maxi, i, queue_active) -> barista:
    if queue_active == True:
        if i < (maxi * div):
            return barista.barista(False, i)
        elif i >= (div * maxi):
            return barista.barista(True, i)
    else:
        return barista.barista(True,i)

"""
Hire (Generate) Instances of baristas (k)
"""


def HumanResources(num_k, div,queue_active):
    K = []
    for i in range(num_k):
        K.append(genBaristas(div, num_k, i, queue_active))
    return K



def main():
    # This looks terrible to look at, but it's all there. 
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--baristanum",
                         help="Number of Baristas",  type=int, default=2)
    parser.add_argument("-n", "--customernum",
                         help="Number of Customers", type=int, default=2)
    parser.add_argument("-num_l", "--line_preset",
                         help="Number of Line Patrons Already in Queue", type=int, default=0)
    parser.add_argument("-num_q", "--queue_preset",
                         help="Number of Queue Patrons Already in Queue", type=int, default=0)
    parser.add_argument(
        "-r", "--rounds",help="Number of Rounds",    type=int, default=200)
    parser.add_argument("-s", "--split", help="Split", type=float, default=0.5)
    parser.add_argument(
        "-a", "--alpha", help="Alpha (conviniece value)", type=float, default=0.8)
    parser.add_argument(
        "-c", "--cost",  help="Cost per order", type=int, default=3)
    parser.add_argument(
        "-b", "--beta",  help="How many to add to the system (Beta)", type=int, default=0.5)
    parser.add_argument(
        "-g", "--gamma", help="How expensive is an expensiver order (Gamma)", type=float, default=1.1)
    parser.add_argument(
        "-l", "--lam",   help="What is the liklihood of a person having an expensive order", type=float, default=0.2)
    parser.add_argument("-filename", "--file_path", help="Where shoudld the output file be saved?",
                        type=str, default="customers_served")  
    parser.add_argument("-save_sim", "--save_sim", help="Should the simulation be saved to an output file?",
                        action=argparse.BooleanOptionalAction, default=False)  
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
    parser.add_argument('--reallocation',             action=argparse.BooleanOptionalAction,
                        default=False, help="Allow Reallocation?")
    parser.add_argument('-use_queue','--queue_active',help="Is GrubHub on or Off",                                   action=argparse.BooleanOptionalAction,default=False)
    parser.add_argument('-use_beta', '--beta_active', help="Add addition (beta) to the number each round or not",    action=argparse.BooleanOptionalAction,default=False)
    parser.add_argument('-preset',   '--preset',      help="Is the simulation based on a test scenario",             action=argparse.BooleanOptionalAction,default=False)
    args = parser.parse_args()

    # All the key variables for the simulations
    num_k      = args.baristanum       # Works
    split      = args.split            # Works 
    custNum    = args.customernum      # Works
    rounds     = args.rounds           # Works
    realloc    = args.reallocation     # Works
    cost       = args.cost             # Works
    alpha      = args.alpha            # Works
    beta       = args.beta             # TODO BETA in progress
    use_beta   = args.beta_active      # TODO Part of BETA 
    gamma      = args.gamma            # Works
    myopic     = args.myopic           # Works
    lam        = args.lam              # Works 
    withGamma  = args.use_gamma        # Works
    Both       = args.both             # Works
    All        = args.all              # Works
    rand       = args.random           # Works
    save_sim   = args.save_sim         # Works
    file_name  = args.file_path        # Works
    use_queue  = args.queue_active     # Should work...
    preset_sim = args.preset
    num_line_patrons_preset  = args.line_preset
    num_queue_patrons_preset = args.queue_preset

    if withGamma == True and not Both and not All and not rand and not preset_sim:
        print("—>Greedy Simulation")
        K = HumanResources(num_k,split,use_queue)
        sim.Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif withGamma == False and not Both and not All and not rand and not preset_sim:  # Default
        print("—>Greedy Simulation")
        K = HumanResources(num_k,split,use_queue)
        sim.Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif Both and not All and not rand and not preset_sim:
        print("—>Greedy Simulation without Gamma")
        K = HumanResources(num_k,split,use_queue)
        sim.Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print("—>Greedy Simulation with Gamma")
        K = HumanResources(num_k,split,use_queue)
        sim.Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif All == True and not preset_sim:
        print("->Random Simulation")
        K = HumanResources(num_k,split,use_queue)
        sim.Random_simulation(K, rounds, 0.5, 1000, custNum, cost, realloc,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print()
        print("—>Greedy Simulation without Gamma")
        K = HumanResources(num_k,split,use_queue)
        sim.Greedy_Simulation(K, rounds, 1000, custNum, cost, realloc, alpha,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
        print()
        print("—>Greedy Simulation with Gamma")
        K = HumanResources(num_k,split,use_queue)
        sim.Gamma_Greedy_Simulation(
            K, rounds, 1000, custNum, cost, realloc, alpha, gamma, lam, myopic,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif rand and not preset_sim:
        print("->Random Simulation")
        K = HumanResources(num_k,split,use_queue)
        sim.Random_simulation(K, rounds, 0.5, 1000, custNum, cost, realloc,use_queue,use_beta,beta)
        printBaristas(K, save_sim, cost, alpha, realloc, file_name,use_queue)
    elif preset_sim:
        K = HumanResources(num_k,split,use_queue)
        sim.PresetSimulation(K,rounds,custNum,cost,realloc,alpha,use_queue,use_beta,beta,num_queue_patrons_preset,num_line_patrons_preset) 
        printBaristas(K, save_sim, cost, alpha, realloc,file_name,use_queue)



  

if __name__ == "__main__":
    main()
