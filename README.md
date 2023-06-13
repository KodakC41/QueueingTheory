# The Starbucks Problem

For a few years working as a barista at Starbucks I wondered about the efficiency of our ordering systems. There were and are now two, online and in-person ordering. 
To better understand this, current research has abstracted this system into a cafe simulator. This simulator has a few parameters. 

1. N — the number of patrons entering the system per clock-time
2. K — the number of baristas serving the patrons in line
3. Alpha — The convenience factor for a person using the Virtual Queue
4. Split — The division of labor between the Virtual and In Person Lines.
5. Rounds — How many "minutes" the simulation should last
6. Cost — How long does each order take in clock time
7. Reallocation — If unoccupied, can baristas from one line help complete orders from the other.
8. Beta — How many more people are allowed to enter the system when the virtual queue is enabled (disabled by default)
9. Gamma — How much more an expensive order cost than a normal order
10. Lambda  — What is the probability of orders being expensive
11. Myopic — Are people in line able to see if a person has an expensive order or not


In examining these parameters we are able to observe how different divisions of labor and perceived conveniences costs can affect a person expected cost for waiting in one 
line over another. 

Here is how to run it

```python
—>Greedy Simulation
Line Baristas served 95 with an average cost of 44
Queue Baristas served 106 with an average cost of 43
```
Where the arguments above are represented in the command-line arguments. 
All of the command-line arguments can be tweaked as follows:

```shell
optional arguments:
  -h, --help            show this help message and exit
  -k BARISTANUM, --baristanum BARISTANUM
                        Number of Baristas
  -n CUSTOMERNUM, --customernum CUSTOMERNUM
                        Number of Customers
  -r ROUNDS, --rounds ROUNDS
                        Number of Rounds
  -s SPLIT, --split SPLIT
                        Split
  --reallocation, --no-reallocation
                        Allow Reallocation? (default: False)
  -a ALPHA, --alpha ALPHA
                        Alpha (conviniece value)
  -c COST, --cost COST  Cost per order
  -b BETA, --beta BETA  How many to add to the system (Beta)
  -g GAMMA, --gamma GAMMA
                        How expensive is an expensiver order (Gamma)
  -l LAM, --lam LAM     What is the liklihood of a person having an expensive order
  -filename FILE_PATH, --file_path FILE_PATH
                        Where shoudld the output file be saved?
  -save_sim, --save_sim, --no-save_sim
                        Should the simulation be saved to an output file? (default: False)
  --use_gamma, --no-use_gamma
                        Use Gamma or not (default: False)
  --myopic, --no-myopic
                        Are Patrons Myopic or not? (default: False)
  --both, --no-both     Run both Greedy case that use gamma or not (default: False)
  --all, --no-all       Run all Simulations (default: False)
  --random, --no-random
                        Run the random simulation (default: False)
  -use_queue, --queue_active, --no-queue_active
                        Is GrubHub on or Off (default: False)
  -use_beta, --beta_active, --no-beta_active
                        Use Beta or not? (default: False)
```