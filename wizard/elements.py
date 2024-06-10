from dataclasses import dataclass
import pprint

@dataclass(order=True, frozen=True)
class Element:
    id: int

class State:
    def __init__(self, elements: list[Element]):
        self.elements = set(elements)
    
    def __repr__(self):
        return f"State({sorted(self.elements)})"

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.elements == other.elements
    
    def __hash__(self):
        elems = list(self.elements)
        elems.sort()
        return hash(tuple(elems))