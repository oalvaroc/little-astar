import wizard as w

import pprint
import json

import graphviz


def load(file) -> dict:
    with open(file) as f:
        return json.load(f)


def transform_dataset(elements: list[map], rules: list[map]):
    newelements = []
    for id in elements:
        newelements.append(w.Element(int(id)))

    newrules = {}
    for rule in rules:
        key = list(rule.keys())[0]
        val = list(rule.values())[0]
        newval = []
        for p1, p2 in val:
            newval.append([w.Element(p1), w.Element(p2)])
        newrules[w.Element(int(key))] = newval

    return newelements, newrules


def element_name(elements: map, elem: w.Element):
    return elements[str(elem.id)]


def plot_solution(solution, goal, elements, cost):
    dot = graphviz.Digraph('Solution', format="png")
    cost = 0

    state = None
    path = []
    for s in solution:
        if goal in s.elements:
            state = s

    path.append(goal)
    while state:
        step = solution[state]
        if step is None:
            break
        path.append(step.rule)
        dot.node(f'_{step.rule[0].id}', element_name(elements, step.rule[0]))
        dot.node(f'_{step.rule[1].id}', element_name(elements, step.rule[1]))
        dot.node(f'_{step.rule[2].id}', element_name(elements, step.rule[2]))
        dot.edge(f'_{step.rule[0].id}', f'_{step.rule[2].id}')
        dot.edge(f'_{step.rule[1].id}', f'_{step.rule[2].id}')
        cost += 1
        state = step.parent

    dot.node(f'_{goal.id}', label=f"{element_name(elements, goal)}\ncost={cost}")
    dot.render('solution')
    pprint.pp(list(reversed(path)))


if __name__ == "__main__":
    rules = load('data/simple-base.json')
    elements_m = load('data/simple-names.json')
    elements, rules = transform_dataset(elements_m, rules)

    n = int(input('goal > '))
    goal = w.Element(n)
    initial = w.State(elements[:4])

    solution, cost = w.astar(initial, goal, rules, elements_m, draw=True)
    plot_solution(solution, goal, elements_m, cost)
