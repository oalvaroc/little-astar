"""
Generate a subset of little alchemy elements
"""
import json

NUM_ELEMENTS = 10

def load(file) -> dict:
    with open(file) as f:
        return json.load(f)

def save(data, file):
    with open(file, 'w+') as f:
        json.dump(data, f)

if __name__ == "__main__":
    base = load("data/base.580.json")
    names = load("data/names.580.json")

    print(f"Original: {len(names)} elements")

    newnames = [{str(i): names[str(i)]} for i in range(1, NUM_ELEMENTS + 1)]

    newbase = []
    for i in range(1, NUM_ELEMENTS + 1):
        parents = base[str(i)].get("parents", [])
        newparents = []
        for p in parents:
            if p[0] < NUM_ELEMENTS and p[1] < NUM_ELEMENTS:
                newparents.append(p)
        newbase.append({str(i): newparents})

    print(f"New: {len(newnames)} elements")

    save(newnames, 'data/simple-names.json')
    save(newbase, 'data/simple-base.json')