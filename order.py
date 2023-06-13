"""
Order class
| The Starbucks Problem: Written for the Univeristy of Rochester Dept. Computer Science
| Spring 2023 
| Contains the Data Struture for orders 
| Issue  |  Initials   |  Date       | Change
|   7    |    CJB      |  06/2023    | Initial Version 
"""
class order:
    start = 0
    person = 1
    ext = 0

    def __init__(self, start, person) -> None:
        self.person = person
        self.start = start