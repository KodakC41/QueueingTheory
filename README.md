# The Starbucks Problem

For a few years working as a barista at Starbucks I wondered about the efficiency of our ordering systems. There were and are now two, online and in-person ordering. 
To better understand this, current research has abstrastacted this system into a cafe simulator. This simulator has a few parameters. 

1. N — the number of patrons entering the system per clock-time
2. K — the number of baristas serving the patrons in line
3. Alpha — The convinience factor for a person using the Vitrual Queue
4. Split — The division of labor between the Virutal and In Person Lines. 
5. Rounds — How many "minutes" the simulation should last
6. Cost — How long does each order take in clock time
7. Reallocation — If unoccupied, can baristas from one line help complete orders from the other.

In examining these parameters we are able to observe how different divisions of labor and percieved conviniences costs can affect a person expected cost for waiting in one 
line over another. 

Here is how to run it

```python
QueueingTheory % python3 StarbucksProblem.py -k 2 -a 0.9 -c 3 -s 0.5 -n 1
—>Greedy Simulation
Line Baristas served 95 with an average cost of 22.16315789473684
Queue Baristas served 105 with an average cost of 19.227169811320756
```

Where the arguments above are represented in the commandline arguments. 
