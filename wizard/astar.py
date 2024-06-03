import heapq
from dataclasses import dataclass, field

from .elements import State, Element

@dataclass(order=True)
class PrioritizedState:
    fscore: int
    state: State = field(compare=False)

levels = {
    Element(1): 0,
    Element(2): 0,
    Element(3): 0,
    Element(4): 0,
}

def level(elem: Element, rules):
    if elem <= Element(4):
        return levels[elem]

    queue = set([elem])
    while queue:
        front = queue.pop()
        parents = rules[front]
        if not parents:
            levels[front] = 0
            continue

        for p1, p2 in parents:
            if not p1 in levels:
                queue.add(p1)
            if not p2 in levels:
                queue.add(p2)

            if p1 in levels and p2 in levels:
                levels[front] = min(levels.get(front, float('inf')), levels[p1] + levels[p2] + 1)
            else:
                queue.add(front)

    return levels[elem]

def heuristic(state: State, goal: Element, rules):
    if goal in state.elements:
        return 0

    state_level = max([levels[elem] for elem in state.elements])
    goal_level = levels[goal]
    if goal_level < state_level:
        return 1
    return goal_level - state_level + 1

def expand(rules, state: State):
    newelements = set()

    for elem, parents in rules.items():
        if elem in state.elements:
            continue

        for p1, p2 in parents:
            if p1 in state.elements and p2 in state.elements:
                newelements.add(elem)

    return newelements

def astar(start: State, goal: State, rules: list):
    opened = []
    openset = set()
    closeset = set()

    # pre-compute levels
    for elem, _ in rules.items():
        level(elem, rules)

    g = {}
    g[start] = 0

    f = {}
    f[start] = heuristic(start, goal, rules)

    solution = {}
    solution[start] = None

    heapq.heappush(opened, PrioritizedState(f[start], start))
    openset.add(start)

    while opened:
        current = heapq.heappop(opened).state
        if goal in current.elements:
            return solution

        for child in expand(rules, current):
            newstate = State([*current.elements, child])
            newg = g[current] + 1
            newf = newg + heuristic(newstate, goal, rules)

            if newstate not in openset and newstate not in closeset:
                g[newstate] = newg
                f[newstate] = newf
                heapq.heappush(opened, PrioritizedState(f[newstate], newstate))
                openset.add(newstate)
                solution[newstate] = current
            elif (newstate in openset or newstate in closeset) and newg < g[newstate]:
                solution[newstate] = current
                f_old = f[newstate]
                g[newstate] = newg
                f[newstate] = newf
                try:
                    openset.remove(newstate)
                    opened.remove(PrioritizedState(f_old, newstate))
                    heapq.heapify(opened)
                    heapq.heappush(opened, PrioritizedState(f[newstate], newstate))
                    closeset.remove(newstate)
                except:
                    pass

        openset.remove(current)
        closeset.add(current)
    
    return solution
