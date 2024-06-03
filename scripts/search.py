import wizard
import json
import pprint

def load(file) -> dict:
    with open(file) as f:
        return json.load(f)

def transform_dataset(elements: list[map], rules: list[map]):
    newelements = []
    for elem in elements:
        key = list(elem.keys())[0]
        value = list(elem.values())[0]
        newelements.append(wizard.Element(int(key)))

    newrules = {}
    for rule in rules:
        key = list(rule.keys())[0]
        val = list(rule.values())[0]
        newval = []
        for p1, p2 in val:
            newval.append([wizard.Element(p1), wizard.Element(p2)])
        newrules[wizard.Element(int(key))] = newval

    return newelements, newrules

def transform_dataset2(elements, rules):
    newelements = []
    for elem in elements.keys():
        newelements.append(wizard.Element(int(elem)))

    newrules = {}
    for key, val in rules.items():
        key = int(key)
        parents = val.get("parents", [])
        newval = []
        for p1, p2 in parents:
            newval.append([wizard.Element(p1), wizard.Element(p2)])
        newrules[wizard.Element(int(key))] = newval

    return newelements, newrules

if __name__ == "__main__":
    rules = load('data/base.580.json')
    elements = load('data/names.580.json')
    elements, rules = transform_dataset2(elements, rules)

    n = int(input('goal > '))

    goal = wizard.Element(n)
    start = wizard.State(elements[:4])
    solution = wizard.astar(start, goal, rules)
    
    state = None
    path = []

    for k in solution.keys():
        if goal in k.elements:
            state = k
            path.append(k)

    while state:
        parent = solution[state]
        path.append(parent)
        state = parent

    pprint.pp(list(reversed(path)))