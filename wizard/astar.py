import heapq
from dataclasses import dataclass, field

from .elements import State, Element, SolutionStep

import graphviz
import math

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

def heuristic_bad(state: State, goal: Element, rules):
    state_level = max([levels[elem] for elem in state.elements])
    return abs(state_level - levels[goal])

def heuristic_good(state: State, goal: Element, rules):
    if goal in state.elements:
        return 0
    state_level = max([levels[elem] for elem in state.elements])
    if state_level > levels[goal]:
        return float('inf')
    
    h = math.log2(levels[goal] - min(2*state_level + 1, levels[goal]) + 1)
    return h + 1

def expand(rules, state: State, goal: Element):
    newelements = set()

    for elem, parents in rules.items():
        if elem in state.elements:
            continue

        if elem.id > goal.id:
            continue

        for p1, p2 in parents:
            if p1 in state.elements and p2 in state.elements:
                if max([levels[i] for i in (state.elements | {elem})]) > levels[goal]:
                    continue

                p1_id, p2_id = sorted([p1.id, p2.id])
                newelements.add((Element(p1_id), Element(p2_id), elem))

    return newelements

def state2dot(state: State, cost, heur, fscore, elem_map: map):
    elem_row = (' | '.join([elem_map[str(e.id)] for e in state.elements]))
    f_row = f"f = {cost} + {heur} = {fscore}"
    return graphviz.nohtml(f"{'{' + elem_row + '}'} | {f_row}")

def astar(start: State, goal: Element, rules: list, elem_map: map, draw=False, admissible=True):
    opened = []
    openset = set()
    closeset = set()

    # pre-compute levels
    for elem, _ in rules.items():
        level(elem, rules)

    print(f'goal level: {levels[goal]} {elem_map[str(goal.id)]}')

    if admissible:
        heuristic = heuristic_good
    else:
        heuristic = heuristic_bad

    g = {}
    g[start] = 0

    f = {}
    f[start] = heuristic(start, goal, rules)

    solution = {}
    solution[start] = None

    heapq.heappush(opened, PrioritizedState(f[start], start))
    openset.add(start)

    best_state = None

    if draw:
        dot = graphviz.Digraph('A* Search Tree', 
                               format="png",
                               node_attr={'shape': 'record'},
                               graph_attr={"rankdir": "LR"})
        dot.node(str(start), state2dot(start, 0, f[start], f[start], elem_map))

    while opened:
        current = heapq.heappop(opened).state
        if goal in current.elements:
            best_state = current
            dot.node(str(current), color="red")
            print(f'found new best: {best_state}')
            break

        for p1, p2, child in expand(rules, current, goal):
            newstate = State(current.elements | {child})

            newg = g[current] + 1
            heur = heuristic(newstate, goal, rules)
            newf = newg + heur

            if newstate not in openset and newstate not in closeset:
                g[newstate] = newg
                f[newstate] = newf
                heapq.heappush(opened, PrioritizedState(f[newstate], newstate))
                openset.add(newstate)
                solution[newstate] = SolutionStep(current, (p1, p2, child))

                if draw:
                    dot.node(str(newstate), state2dot(newstate, newg, heur, newf, elem_map))
                    dot.edge(str(current), str(newstate))

            elif newg < g[newstate]:
                solution[newstate] = SolutionStep(current, (p1, p2, child))
                f_old = f[newstate]
                g[newstate] = newg
                f[newstate] = newf
                try:
                    openset.remove(newstate)
                    opened.remove(PrioritizedState(f_old, newstate))
                    heapq.heapify(opened)
                    heapq.heappush(opened, PrioritizedState(f[newstate], newstate))
                    openset.add(newstate)
                    closeset.remove(newstate)

                    if draw:
                        dot.node(str(newstate), state2dot(newstate, newg, heur, newf, elem_map))
                        dot.edge(str(current), str(newstate))
                except:
                    pass

        openset.remove(current)
        closeset.add(current)

    if draw:
        dot.render(f'astar-tree-{elem_map[str(goal.id)]}')

    return solution, g.get(best_state, float('inf'))
