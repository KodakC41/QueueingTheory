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
8. Gamma — How much more an expensive order cost than a normal order
9. Prob  — What is the probability of orders being expensive 
10. Myopic — Are people in line able to see if a person has an expensive order or not

In examining these parameters we are able to observe how different divisions of labor and perceived conveniences costs can affect a person expected cost for waiting in one 
line over another. 

Here is how to run it

```python
—>Greedy Simulation
Line Baristas served 95 with an average cost of 44
Queue Baristas served 106 with an average cost of 43
```

Where the arguments above are represented in the command-line arguments. 
