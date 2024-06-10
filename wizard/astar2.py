from collections import deque, defaultdict
import heapq
from wizard.elements import Element, State

from dataclasses import dataclass, field

@dataclass(order=True)
class PrioritizedState:
    fscore: int
    state: State = field(compare=False)


def element_children(goal, rules, children: map):
    tosearch = set([goal])
    elements = set()

    while tosearch:
        elem = tosearch.pop()
        if elem in elements:
            continue

        parents = rules[elem]
        elements.add(elem)
    
        for p1, p2 in parents:
            tosearch.add(p1)
            tosearch.add(p2)

            if p1 in children:
                children[p1].add((elem, p2))
            else:
                children[p1] = set([(elem, p2)])
    
            if p2 in children:
                children[p2].add((elem, p1))
            else:
                children[p2] = set([(elem, p1)])

    return children

def bfs_final_state(initial_state, rules, goal):
    shortest_paths = defaultdict(lambda: None)
    queue = deque([(elem, initial_state) for elem in initial_state.elements])
    visited = set()

    while queue:
        current, state = queue.popleft()
        if current == goal:
            return state
    
        for elem in next_elems(state, rules):
            newstate = State(state.elements | {elem})
            if newstate not in visited:
                visited.add(newstate)
                queue.append((elem, newstate))
                if elem not in shortest_paths or len(newstate.elements) < len(shortest_paths[elem].elements):
                    shortest_paths[elem] = newstate

    return None

def heuristic(state, final_state):
    return len(final_state.elements - state.elements)

def next_elems(state, rules):
    nextelems = set()
    for elem, parents in rules.items():
        if elem in state.elements:
            continue

        for p1, p2 in parents:
            if p1 in state.elements and p2 in state.elements:
                nextelems.add(elem)
    return nextelems
    
def next_states(state, rules):
    nextstates = set()
    for elem, parents in rules.items():
        if elem in state.elements:
            continue

        for p1, p2 in parents:
            if p1 in state.elements and p2 in state.elements:
                nextstate = State(state.elements | {elem})
                nextstates.add((p1, p2, nextstate))
    return nextstates
    
def astar(initial_state, final_state, rules):
    opened = []
    openset = set()
    closed = set()
    f = {}
    g = {}

    g[initial_state] = 0
    f[initial_state] = heuristic(initial_state, final_state)

    heapq.heappush(opened, PrioritizedState(f[initial_state], initial_state))
    openset.add(initial_state)

    solution = { initial_state: None }

    while opened:
        current = heapq.heappop(opened)
        state = current.state
        openset.remove(state)

        if state == final_state:
            return solution
        
        for p1, p2, nextstate in next_states(state, rules):
            newg = g[state] + 1
            newf = newg + heuristic(nextstate, final_state)

            if nextstate not in openset and nextstate not in closed:
                f[nextstate] = newf
                g[nextstate] = newg
                openset.add(nextstate)
                heapq.heappush(opened, PrioritizedState(f[nextstate], nextstate))
                solution[nextstate] = (p1, p2, state)
            elif newg < g[nextstate]:
                f_old = f[nextstate]
                f[nextstate] = newf
                g[nextstate] = newg
                
                try:
                    opened.remove(PrioritizedState(f_old, nextstate))
                    openset.remove(nextstate)

                    heapq.heapify(opened)
                    heapq.heappush(opened, PrioritizedState(f[nextstate], nextstate))
                    openset.add(nextstate)

                    closed.remove(nextstate)

                    solution[nextstate] = (p1, p2, state)
                except KeyError:
                    pass
                except ValueError:
                    pass
        
        closed.add(state)

    return solution

def build_path(final_state, solution):
    path = []
    state = final_state

    if final_state not in solution:
        return []
    
    while state:
        sol = solution[state]
        if sol is None:
            break
        p1, p2, parent = sol
        path.append((p1, p2, state))
        state = parent
    
    return list(reversed(path))
