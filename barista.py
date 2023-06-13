"""
Barista class
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| Contains the Data Struture for Baristas (k)
| Issue  |  Initials   |  Date       | Change
|   7    |    CJB      |  06/2023    | Initial Version 
"""
class barista:
    indent = 1  # (Again) UUID may be a little overkill
    line = bool()          # True or false depending on which line a person is in
    occupied = bool()      # Is this barista currently serving anyone?
    # A list of the people a barista has served as an array of N patrons (n)
    service_time = []

    def __init__(self, line, i) -> None:
        self.ident = i
        self.line = line
        self.service_time = []
        self.occupied = False

    def setOccupied(self, b) -> None:
        self.occupied = b
