"""
Patrons class
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| Contains the Data Struture for patrons
| Issue  |  Initials   |  Date       | Change
|   7    |    CJB      |  06/2023    | Initial Version 
"""
class patron:
    ident = 0       # UUID might be a little overkill
    line = bool()              # which line a patron is in
    enter = int()              # The Time at which the patron enters.
    cost = 5                   # An agent's associated cost for waiting in line
    beingServed = False        # Is a Patron being served
    alpha = 0.8                # is part of the virtual Queue only
    gamma = 1.2                # The Gamma component that makes an order more expensive by time
    hasExpensiveOrder = bool() # does Gamma come in account?

    def __init__(self, line, enter, cost, exp=False, gam=1) -> None:
        self.ident = 0
        self.line = line
        self.enter = enter
        self.ext = 0
        self.gamma = gam
        if exp:
            self.hasExpensiveOrder = True
            self.cost = cost * self.gamma
        else:
            self.cost = cost

    def setBeingServed(self, b) -> None:
        self.beingServed = b

    def is_being_served(self) -> bool:
        return self.beingServed

    def setLine(self, l) -> None:
        self.line = l

    def hasExpensive(self) -> None:
        return self.hasExpensiveOrder