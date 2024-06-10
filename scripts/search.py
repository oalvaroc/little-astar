import wizard
import wizard.heuristic as wh
import wizard.astar2 as wa

import pprint
import json
import os


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
    initial = wizard.State(elements[:4])

    if not os.path.exists('final-states.json'):
        final_states = {}
        print('generating final-states.json')
        for elem in elements:        
            print(f'searching final state {elem}')
            final_states[elem] = wa.bfs_final_state(initial, rules, elem)

        with open('final-states.json', 'w+') as f:
            obj = {}
            for elem in final_states:
                state = final_states[elem]
                d = [e.id for e in state.elements]
                d.sort()
                obj[f'{elem.id}'] = d
            json.dump(obj, f)

    with open('final-states.json') as f:
        final_states = json.load(f)

    final_state = wizard.State([wizard.Element(int(i)) for i in final_states[f'{goal.id}']])
    print(f'final state: {final_state}')
    solution = wa.astar(initial, final_state, rules)

    print('solution:')
    pprint.pp(wa.build_path(final_state, solution), indent=2)

    with open('solution.txt', 'w+') as f:
        for k, v in solution.items():
            f.write(f"{k}: {v}\n")